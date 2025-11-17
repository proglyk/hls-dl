## hls-dl
Universal utility for downloading video from HLS streams (HTTP Live Streaming). \

P.S. Project under development. API not stable. Uses for your own risks

### Features
- ✅ Download standard m3u8 playlists
- ✅ Support for protected streams with custom encryption
- ✅ Video quality selection
- ✅ Batch download
- ✅ Extensible extractor architecture
- ✅ XOR/AES decryption

### Requirements
```
pip install requests lxml pycryptodome
```

FFmpeg must be installed and available in PATH.

### Installation
```
git clone https://github.com/proglyk/hls-dl.git
cd hls-dl
pip install -r requirements.txt
```

### Usage

#### Standard HLS stream
```
python main.py https://test1.flashphoner.com:8445/test/test.m3u8
```

#### Quality selection
```
python main.py https://test1.flashphoner.com:8445/test/test.m3u8 -r 1280x720
```

#### Protected stream
```sh
python main.py https://play.boomstream.com/VCcNtuiw -k "your_xor_key" -o video.mp4
```

#### Batch download
```sh
python main.py -i urls.txt -o downloads/
```

`urls.txt` format:
```
https://example.com/video1.m3u8
https://example.com/video2.m3u8
https://example.com/video3.m3u8
```

### Architecture
```
hls-dl/
    core/
        crypto.py          # Cryptographic utilities
        downloader.py      # Base downloader
    extractors/
        base.py            # Base extractor class
        generic.py         # For standard m3u8
        protected.py       # For protected streams
        boomstream.py      # For Boomstream (optional)
    main.py                # CLI interface
    requirements.txt
    README.md
```

### Creating your own extractor
```python
from extractors.base import BaseExtractor

class MyExtractor(BaseExtractor):
    def extract(self):
        # Your logic for extracting m3u8 URL
        return {
            'm3u8_url': 'https://...',
            'title': 'video_title',
            'headers': {'Referer': '...'}
        }

    @staticmethod
    def can_handle(url):
        return 'myservice.com' in url
```

### License
MIT License

### Disclaimer
This utility is intended for educational purposes only.
Respect copyrights and content usage terms.
