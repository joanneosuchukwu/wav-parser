import sys
import struct

def parse_wav(path):
  with open(path, 'rb') as f:
    #container format
    chunk_id = f.read(4).decode()
    #size of container format
    chunk_size = struct.unpack("<I", f.read(4))[0]

    #file format
    riff_format = f.read(4).decode()

    #basic validation, stop early if this isn't actually a wav file
    if chunk_id != 'RIFF' or riff_format != 'WAVE':
      print("not a valid wav file: ", path)
      return None

    #keep reading chunks til we hit fmt. skips junk, list, fact, whatever else shows up
    junk = None
    junk_size = 0
    next_id = f.read(4).decode()
    while next_id != 'fmt ':
      next_size = struct.unpack("<I", f.read(4))[0]
      if next_id == 'JUNK':
        junk = next_id
        junk_size = next_size
      #skip this chunk's data
      f.seek(next_size, 1)
      #chunks are padded to an even byte boundary
      if next_size % 2:
        f.seek(1, 1)
      next_id = f.read(4).decode()

    #metadata and technical specifications
    sub_chunk1_id = next_id

    #format chunk size
    sub_chunk1_size = struct.unpack("<I", f.read(4))[0]

    #encoding method. 1 means PCM; desirable for clinical signal processing
    audio_format = struct.unpack("<H", f.read(2))[0]

    # number of channels: mono vs stereo
    num_channels = struct.unpack("<H", f.read(2))[0]

    #sample rate (obeys nyqist, usually)
    sample_rate = struct.unpack("<I", f.read(4))[0]

    #average number of bytes of audio data processed per second: num_channels * bits_per_sample/8 * sample_rate
    byte_rate = struct.unpack("<I", f.read(4))[0]

    #number of bytes per sample frame across all channels, num_channels * bits_per_sample/8
    block_align = struct.unpack("<H", f.read(2))[0]

    #how many bits in one sampl
    bits_per_sample = struct.unpack("<H", f.read(2))[0]

    #extended/non-pcm formats have extra fmt fields past the standard 16 bytes, skip them
    fmt_extra = sub_chunk1_size - 16
    if fmt_extra > 0:
      f.seek(fmt_extra, 1)

    #same deal, keep reading til data shows up
    next_id = f.read(4).decode()
    while next_id != 'data':
      next_size = struct.unpack("<I", f.read(4))[0]
      f.seek(next_size, 1)
      #chunks are padded to an even byte boundary
      if next_size % 2:
        f.seek(1, 1)
      next_id = f.read(4).decode()

    # data
    sub_chunk2_id = next_id
    #size of data chunk
    sub_chunk2_size = struct.unpack("<I", f.read(4))[0]

    #number of frames
    num_frames = sub_chunk2_size//block_align

    #duration in seconds
    duration_in_seconds = num_frames/sample_rate

    #actual audio data in binary
    raw_audio_data = f.read(sub_chunk2_size)

  return {
    "chunk_id": chunk_id,
    "chunk_size": chunk_size,
    "riff_format": riff_format,
    "junk": junk,
    "junk_size": junk_size,
    "sub_chunk1_id": sub_chunk1_id,
    "sub_chunk1_size": sub_chunk1_size,
    "audio_format": audio_format,
    "num_channels": num_channels,
    "sample_rate": sample_rate,
    "byte_rate": byte_rate,
    "block_align": block_align,
    "bits_per_sample": bits_per_sample,
    "sub_chunk2_id": sub_chunk2_id,
    "sub_chunk2_size": sub_chunk2_size,
    "num_frames": num_frames,
    "duration_in_seconds": duration_in_seconds,
    "raw_audio_data": raw_audio_data
  }

#accepts a file path from the command line, defaults to sample.wav
path = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"
specs = parse_wav(path)

if specs:
  print("chunk id: ", specs["chunk_id"])
  print("chunk size: ", specs["chunk_size"])
  print("riff format: ", specs["riff_format"])
  print("junk: ", specs["junk"])
  print("junk size: ", specs["junk_size"])
  print("subchunk1 id: ", specs["sub_chunk1_id"])
  print("subchunk1 size: ", specs["sub_chunk1_size"])
  print("audio format: ", specs["audio_format"])
  print("number of channels: ", specs["num_channels"])
  print("sample rate: ", specs["sample_rate"])
  print("byte rate: ", specs["byte_rate"])
  print("block align: ", specs["block_align"])
  print("bits per sample: ", specs["bits_per_sample"])
  print("subchunk2 id: ", specs["sub_chunk2_id"])
  print("subchunk2 size: ", specs["sub_chunk2_size"])
  print("number of frames: ", specs["num_frames"])
  print("duration in seconds: ", specs["duration_in_seconds"])
  print("raw audio data: ", specs["raw_audio_data"][:10])
