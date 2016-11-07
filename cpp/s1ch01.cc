/*
Cryptopals set 1 challenge 1

Convert hex to base64

The string:
49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
Should produce:
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
*/
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

vector<uint8_t> hex2binary(const string & input) {
  // Check input string
  if(string::npos != input.find_first_not_of("0123456789ABCDEFabcdef")) {
    return {};
  }

  union {
    uint64_t binary;
    char byte[8];
  } value{};

  int input_size = input.size();
  int offset = (input_size % 16);

  vector<uint8_t> result{};
  result.reserve((input_size + 1) / 2);

  if (offset) {
    value.binary = stoull(input.substr(0, offset), nullptr, 16);
    for (auto index = (offset + 1) / 2; index--; ) {
        result.emplace_back(value.byte[index]);
    }
  }

  for (; offset < input_size; offset += 16) {
    value.binary = stoull(input.substr(offset, 16), nullptr, 16);
    for(auto index = 8; index--;) {
      result.emplace_back(value.byte[index]);
    }
  }
  return result;
}

string binary2hex(const vector<uint8_t> input) {
  char hex_elements[] = "0123456789abcdef";
  stringstream result;
  for(uint8_t byte: input) {
    result << hex_elements[byte >> 4] << hex_elements[byte % 16];
  }
  return result.str();
}

vector<uint8_t> base642binary(const string & input) {
  string base64_elements = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  vector<uint8_t> result{};
  if (input.size() % 4 != 0) {
    return result;
  }
  for (int i = 0; i < input.size(); i += 4) {
    int b[4];
    for (int j = 0; j < 4; j++) {
      if (base64_elements.find(input[i + j]) != string::npos) {
        b[j] = base64_elements.find(input[i + j]);
      } else {
        b[j] = 0;
      }
    }

    result.emplace_back(b[0] << 2 | b[1] >> 4);
    result.emplace_back((b[1] & 15) << 4 | b[2] >> 2);
    result.emplace_back((b[2] & 3) << 6 | b[3]);
  }
  return result;
}

string binary2base64(const vector<uint8_t> input) {
  char base64_elements[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  stringstream result;
  int tmp;
  for (int i = 0; i < input.size(); i += 3) {
    result << base64_elements[input[i] >> 2];
    tmp = (input[i] & 3) << 4; // Get two last bits of byte
    if ((i + 1) < input.size()) {
      tmp |= input[i + 1] >> 4;
      result << base64_elements[tmp];
      tmp = (input[i + 1] & 15) << 2;
      if((i + 2) < input.size()) {
        tmp |= input[i + 2] >> 6;
        result << base64_elements[tmp];
        result << base64_elements[input[i + 2] & 63];
      } else {
        result << base64_elements[tmp] << "=";
      }
    } else {
      result << base64_elements[tmp] << "==";
    }
  }
  return result.str();
}

int main() {
  cout<<binary2base64(hex2binary(
    "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
  ))<<endl;
  return 0;
}
