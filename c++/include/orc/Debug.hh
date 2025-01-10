#pragma once

#include "Common.hh"

#include <array>
#include <vector>

namespace orc {
  struct BiuRunLengthInfo {
    std::size_t bitWidth{};
    std::size_t numElements{};
    std::size_t encodedBytes{};
    std::string encodeKind{};
  };

  struct BiuRowGroupInfo {
    std::size_t offsetFromStream{};
    std::size_t numElementsToSkip{};
    std::size_t numElementsToRemain{};
  };

  class Reader;

  class Debugger {
   public:
    static Debugger& instance();
    void check();
    void incrementRGIdx();
    void setIsSec(bool flag);
    bool isSec();
    void addNewRL(std::size_t bitWidth, std::size_t numElements, std::string encodeKind);
    void resetByteCounter();
    void incrementByteCounter();
    void postProcess();

    std::size_t getRowGroupStride();
    void setRowGroupStride(std::size_t rowGroupStride);

    void getInfoFromReader(Reader* reader);
    void getRowGroupEntryInfo(const std::array<std::size_t, 4>& positionArray);

    void setCustomMaxLiteralSize(const std::vector<std::size_t>& customMaxLiteralSizeSec,
                                 const std::vector<std::size_t>& customMaxLiteralSizeNanosec);
    void updateCustomMaxLiteralSize();
    std::size_t getCustomMaxLiteralSize();

    void enableCustomMaxLiteralSize(bool flag);

    // The null data in CSV may be "", represented as a string "\"\"".
    // If this happens, change it to "". Otherwise, return the original string.
    static std::string handleSpecialNullData(const std::string& s);

   private:
    Debugger();
    ~Debugger() = default;
    Debugger(const Debugger&) = delete;
    Debugger operator=(const Debugger&) = delete;
    int _rowGroupIdx{-1};
    bool _isSec{true};
    int64_t _byteCounter{0};
    std::vector<BiuRunLengthInfo> _rlInfoSec;
    std::vector<BiuRunLengthInfo> _rlInfoNanosec;
    std::vector<BiuRowGroupInfo> _rgInfoSec;
    std::vector<BiuRowGroupInfo> _rgInfoNanosec;
    std::size_t _rowGroupStride;
    std::size_t _streamOffsetFromFileSec;
    std::size_t _streamBytesSec;
    std::size_t _streamOffsetFromFileNanosec;
    std::size_t _streamBytesNanosec;

    bool _enableCustomMaxLiteralSize{false};
    std::vector<std::size_t> _customMaxLiteralSizeSec;
    std::vector<std::size_t> _customMaxLiteralSizeNanosec;
    std::size_t _customLimitConsumedSec;
    std::size_t _customLimitConsumedNanosec;
  };
}  // namespace orc