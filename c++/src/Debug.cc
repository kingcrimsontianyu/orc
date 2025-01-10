#include <orc/Debug.hh>
#include <orc/Reader.hh>
#include "RLEv2.hh"

#include <iomanip>
#include <iostream>
#include <sstream>

namespace orc {
  Debugger& Debugger::instance() {
    static Debugger obj;
    return obj;
  }

  Debugger::Debugger() : _rowGroupStride(10000) {}

  void Debugger::incrementRGIdx() {
    ++_rowGroupIdx;
  }

  void Debugger::setIsSec(bool flag) {
    _isSec = flag;
  }

  bool Debugger::isSec() {
    return _isSec;
  }

  void Debugger::resetByteCounter() {
    _byteCounter = 0;
  }

  void Debugger::incrementByteCounter() {
    ++_byteCounter;
  }

  void Debugger::addNewRL(std::size_t bitWidth, std::size_t numElements, std::string encodeKind) {
    BiuRunLengthInfo b;
    // b.offsetFromStreamStart
    b.bitWidth = bitWidth;
    b.numElements = numElements;

    if (encodeKind == "DIRECT") {
      // 2-byte header
      b.encodedBytes = 2 + b.bitWidth / 8 * b.numElements;
    } else if (encodeKind == "SHORT_REPEAT") {
      // 1-byte header
      b.encodedBytes = 1 + _byteCounter;
    } else if (encodeKind == "DELTA") {
      // 2-byte header
      b.encodedBytes = 2 + _byteCounter;
    } else if (encodeKind == "PATCHED_BASE") {
      // 4-byte header
      b.encodedBytes = 4 + _byteCounter;
    }

    b.encodeKind = encodeKind;

    if (_isSec) {
      _rlInfoSec.push_back(std::move(b));
    } else {
      _rlInfoNanosec.push_back(std::move(b));
    }
  }

  void Debugger::postProcess() {}

  void Debugger::check() {
    {
      std::cout << "--> SECOND\n";
      std::cout << "    offset: " << _streamOffsetFromFileSec << "\n";
      std::cout << "    bytes: " << _streamBytesSec << "\n";
      std::cout << "--> NANOSECOND\n";
      std::cout << "    offset: " << _streamOffsetFromFileNanosec << "\n";
      std::cout << "    bytes: " << _streamBytesNanosec << "\n";
    }

    auto checkSumValue = [](const std::vector<BiuRunLengthInfo>& v) {
      uint64_t sum1 = 0;
      uint64_t sum2 = 0;
      for (const auto& el : v) {
        sum1 += el.numElements;
        sum2 += el.encodedBytes;
      }
      std::cout << "    Total run-length: " << sum1 << "\n";
      std::cout << "    Total encoded length: " << sum2 << "\n";
    };

    std::cout << "--> SECOND\n";
    checkSumValue(_rlInfoSec);
    std::cout << "--> NANOSECOND\n";
    checkSumValue(_rlInfoNanosec);

    auto getExpectedRowGroupInfo =
        [this](const std::vector<BiuRunLengthInfo>& rlVec) -> std::vector<BiuRowGroupInfo> {
      std::vector<BiuRowGroupInfo> res;
      std::size_t numRowsAcc = 0;
      std::size_t bytesAcc = 0;
      for (std::size_t i = 0; i < rlVec.size(); ++i) {
        std::size_t numRowsByRuns = numRowsAcc + rlVec[i].numElements;
        std::size_t numRowsbByRowGroups = _rowGroupStride * res.size();
        if (numRowsByRuns > numRowsbByRowGroups) {
          BiuRowGroupInfo rg{};
          rg.offsetFromStream = bytesAcc;
          rg.numElementsToSkip = numRowsbByRowGroups - numRowsAcc;
          rg.numElementsToRemain = rlVec[i].numElements - rg.numElementsToSkip;
          res.push_back(rg);
        }
        numRowsAcc += rlVec[i].numElements;
        bytesAcc += rlVec[i].encodedBytes;
      }
      return res;
    };
    std::vector<BiuRowGroupInfo> rgInfoSecExpected = getExpectedRowGroupInfo(_rlInfoSec);
    std::vector<BiuRowGroupInfo> rgInfoNanosecExpected = getExpectedRowGroupInfo(_rlInfoNanosec);

    auto compareActualAndExpected = [](const std::vector<BiuRowGroupInfo>& actual,
                                       const std::vector<BiuRowGroupInfo>& expected) {
      std::cout << "rowGroupIdx,\n"
                << "offsetFromStream_actual,\n"
                << "numElementsToSkip_actual,\n"
                << "offsetFromStream_expected,\n"
                << "numElementsToSkip_expected,\n";

      for (std::size_t i = 0; i < actual.size(); ++i) {
        std::cout << std::setw(6) << i << "," << std::setw(16) << actual[i].offsetFromStream << ","
                  << std::setw(16) << actual[i].numElementsToSkip << "," << std::setw(16)
                  << expected[i].offsetFromStream << "," << std::setw(16)
                  << expected[i].numElementsToSkip << "\n";
        if (actual[i].offsetFromStream != expected[i].offsetFromStream ||
            actual[i].numElementsToSkip != expected[i].numElementsToSkip) {
          std::cout << "--------------[ERROR]Data discrepancy!!!!!!--------------\n";
        }
      }
    };
    std::cout << "--> SECOND\n";
    compareActualAndExpected(_rgInfoSec, rgInfoSecExpected);
    std::cout << "--> NANOSECOND\n";
    compareActualAndExpected(_rgInfoNanosec, rgInfoNanosecExpected);

    // Compare SECOND and NANOSECOND
    {
      std::cout << "--> Compare SECOND and NANOSECOND remaining elements\n";
      std::cout << "rowGroupIdx,\n"
                << "numElementsToSkip_SECOND,\n"
                << "numElementsToSkip_NANOSECOND,\n"
                << "numElementsToRemain_SECOND,\n"
                << "numElementsToRemain_NANOSECOND,\n"
                << "doesNanosecHaveMoreOrEqualRemaining\n";
      for (std::size_t i = 0; i < rgInfoSecExpected.size(); ++i) {
        std::cout << std::setw(6) << i << "," << std::setw(16)
                  << rgInfoSecExpected[i].numElementsToSkip << "," << std::setw(16)
                  << rgInfoNanosecExpected[i].numElementsToSkip << "," << std::setw(16)
                  << rgInfoSecExpected[i].numElementsToRemain << "," << std::setw(16)
                  << rgInfoNanosecExpected[i].numElementsToRemain << "," << std::setw(16)
                  << (rgInfoSecExpected[i].numElementsToRemain <=
                      rgInfoNanosecExpected[i].numElementsToRemain)
                  << "\n";
      }
    }

    auto printVerboseInfo = [this](const std::vector<BiuRunLengthInfo>& rlVec) {
      std::size_t numRowsAcc = 0;
      std::size_t rowGroupIdx = 0;
      for (std::size_t i = 0; i < rlVec.size(); ++i) {
        std::size_t numRowsByRuns = numRowsAcc + rlVec[i].numElements;
        std::size_t numRowsbByRowGroups = _rowGroupStride * rowGroupIdx;

        std::cout << "    " << std::setw(16) << rlVec[i].encodeKind << std::setw(10)
                  << rlVec[i].numElements;
        if (rlVec[i].numElements != 512) {
          std::cout << " (not 512)";
        }

        if (numRowsByRuns > numRowsbByRowGroups) {
          std::size_t numElementsToSkip = numRowsbByRowGroups - numRowsAcc;
          std::size_t numElementsToRemain = rlVec[i].numElements - numElementsToSkip;
          std::cout << " --- Row group index: " << rowGroupIdx
                    << ", skipping: " << numElementsToSkip
                    << ", remaining: " << numElementsToRemain;
          ++rowGroupIdx;
        }

        std::cout << "\n";
        numRowsAcc += rlVec[i].numElements;
      }
    };
    std::cout << "--> Verbose info\n";
    std::cout << "--> SECOND\n";
    printVerboseInfo(_rlInfoSec);
    std::cout << "--> NANOSECOND\n";
    printVerboseInfo(_rlInfoNanosec);
  }

  std::size_t Debugger::getRowGroupStride() {
    return _rowGroupStride;
  }

  void Debugger::setRowGroupStride(std::size_t rowGroupStride) {
    _rowGroupStride = rowGroupStride;
  }

  void Debugger::getInfoFromReader(Reader* reader) {
    auto stripeInfo = reader->getStripe(0);

    for (std::size_t i = 0; i < stripeInfo->getNumberOfStreams(); ++i) {
      auto streamInfo = stripeInfo->getStreamInformation(i);
      if (streamInfo->getKind() == StreamKind::StreamKind_DATA) {
        _streamOffsetFromFileSec = streamInfo->getOffset();
        _streamBytesSec = streamInfo->getLength();
      } else if (streamInfo->getKind() == StreamKind::StreamKind_SECONDARY) {
        _streamOffsetFromFileNanosec = streamInfo->getOffset();
        _streamBytesNanosec = streamInfo->getLength();
      }
    }

    auto stripeStats = reader->getStripeStatistics(0);
  }

  void Debugger::getRowGroupEntryInfo(const std::array<std::size_t, 4>& positionArray) {
    BiuRowGroupInfo rgSec;
    rgSec.offsetFromStream = positionArray[0];
    rgSec.numElementsToSkip = positionArray[1];
    _rgInfoSec.push_back(std::move(rgSec));

    BiuRowGroupInfo rgNanosec;
    rgNanosec.offsetFromStream = positionArray[2];
    rgNanosec.numElementsToSkip = positionArray[3];
    _rgInfoNanosec.push_back(std::move(rgNanosec));
  }

  void Debugger::setCustomMaxLiteralSize(
      const std::vector<std::size_t>& customMaxLiteralSizeSec,
      const std::vector<std::size_t>& customMaxLiteralSizeNanosec) {
    _customMaxLiteralSizeSec = customMaxLiteralSizeSec;
    _customMaxLiteralSizeNanosec = customMaxLiteralSizeNanosec;

    _customLimitConsumedSec = 0;
    _customLimitConsumedNanosec = 0;
  }

  std::size_t Debugger::getCustomMaxLiteralSize() {
    if (!_enableCustomMaxLiteralSize) return MAX_LITERAL_SIZE;

    std::size_t ans{};
    if (_isSec) {
      if (_customLimitConsumedSec >= _customMaxLiteralSizeSec.size()) {
        ans = MAX_LITERAL_SIZE;
      } else {
        ans = _customMaxLiteralSizeSec[_customLimitConsumedSec];
      }
    } else {
      if (_customLimitConsumedNanosec >= _customMaxLiteralSizeNanosec.size()) {
        ans = MAX_LITERAL_SIZE;
      } else {
        ans = _customMaxLiteralSizeNanosec[_customLimitConsumedNanosec];
      }
    }

    return ans;
  }

  void Debugger::updateCustomMaxLiteralSize() {
    if (_isSec) {
      if (_customLimitConsumedSec < _customMaxLiteralSizeSec.size()) {
        ++_customLimitConsumedSec;
      }
    } else {
      if (_customLimitConsumedNanosec < _customMaxLiteralSizeNanosec.size()) {
        ++_customLimitConsumedNanosec;
      }
    }
  }

  void Debugger::enableCustomMaxLiteralSize(bool flag) {
    _enableCustomMaxLiteralSize = flag;
  }

  std::string Debugger::handleSpecialNullData(const std::string& s) {
    if (s == "\"\"") {
      return "";
    }
    return s;
  }
}  // namespace orc