import struct
path = "sample.wav"

with open(path, 'rb') as f:
  #container format
  chunk_id = f.read(4).decode()
  #size of container format
  chunk_size = struct.unpack("<I", f.read(4))[0]
  
  #file format
  riff_format = f.read(4).decode()
  
  #check for junk and junk size
  junk = f.read(4).decode()
  junk_size = struct.unpack("<I", f.read(4))[0]
  #skip the junk
  f.seek(junk_size, 1)
  
  #metadata and technical specifications
  sub_chunk1_id = f.read(4).decode()
  #format chunk size
  sub_chunk1_size = struct.unpack("<I", f.read(4))[0]
  
  #encoding method. 1 means PCM; desirable for clinical signal processing
  audio_format = struct.unpack("<H", f.read(2))[0]
  
  #number of channels: mono vs stereo
  num_channels = struct.unpack("<H", f.read(2))[0]
  
  #sample rate (obeys nyqist, usually)
  sample_rate = struct.unpack("<I", f.read(4))[0]
  
  #average number of bytes of audio data processed per second: num_channels * bits_per_sample/8 * sample_rate
  byte_rate = struct.unpack("<I", f.read(4))[0]
  
  #number of bytes per sample frame across all channels, num_channels * bits_per_sample/8
  block_align = struct.unpack("<H", f.read(2))[0]
  
  #how many bits in one sample
  bits_per_sample = struct.unpack("<H", f.read(2))[0]
  
  #data
  sub_chunk2_id = f.read(4).decode()
  #size of data chunk
  sub_chunk2_size = struct.unpack("<I", f.read(4))[0]

  #number of frames
  num_frames = sub_chunk2_size//block_align

  #duration in seconds
  duration_in_seconds = num_frames/sample_rate
  
  #actual audio data in binary
  raw_audio_data = f.read(sub_chunk2_size)

print("chunk id: ", chunk_id)
print("chunk size: ", chunk_size)
print("riff format: ", riff_format)
print("junk: ", junk)
print("junk size: ", junk_size)
print("subchunk1 id: ", sub_chunk1_id)
print("subchunk1 size: ", sub_chunk1_size)
print("audio format: ", audio_format)
print("number of channels: ", num_channels)
print("sample rate: ", sample_rate)
print("byte rate: ", byte_rate)
print("block align: ", block_align)
print("bits per sample: ", bits_per_sample)
print("subchunk2 id: ", sub_chunk2_id)
print("subchunk2 size: ", sub_chunk2_size)
print("number of frames: ", num_frames)
print("duration in seconds: ", duration_in_seconds)
print("raw audio data: ", raw_audio_data[:10])