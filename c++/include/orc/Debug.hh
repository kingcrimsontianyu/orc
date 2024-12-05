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

    void getInfoFromReader(Reader* reader);
    void getRowGroupEntryInfo(const std::array<std::size_t, 4>& positionArray);

   private:
    Debugger() = default;
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
    std::size_t _rowGroupStride{10000};
    std::size_t _streamOffsetFromFileSec;
    std::size_t _streamBytesSec;
    std::size_t _streamOffsetFromFileNanosec;
    std::size_t _streamBytesNanosec;
  };
}  // namespace orc