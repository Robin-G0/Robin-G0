"""Documented path exclusions for filtered line-edit activity, not authorship."""

VERSION = 1
EXCLUDED_DIRS = (
    'datasets', 'dataset', 'models', 'networks', 'node_modules', 'vendor', 'vendors',
    'third_party', 'third-party', 'external', 'extern', 'deps', 'dependencies',
    'build', 'dist', 'out', 'target', 'coverage', 'htmlcov', '.venv', 'venv',
    '__pycache__', '.next', '.nuxt', '.cache', 'generated', '_generated',
    'site-packages', 'CMakeFiles',
)
EXCLUDED_FILES = (
    '*.nn', '*.onnx', '*.tflite', '*.pt', '*.pth', '*.h5', '*.hdf5', '*.pkl',
    '*.pickle', '*.safetensors', '*.csv', '*.tsv', '*.jsonl', '*.ndjson', '*.npy',
    '*.npz', '*.parquet', '*.arrow', '*.feather', '*.sqlite', '*.sqlite3', '*.db',
    '*.svg', '*.ppm', '*.pgm', '*.pbm', '*.pnm', '*.png', '*.jpg', '*.jpeg', '*.gif',
    '*.webp', '*.ico', '*.pdf', '*.mp4', '*.mp3', '*.wav', '*.zip', '*.tar', '*.gz',
    '*lock.json', '*.lock', 'pnpm-lock.yaml', 'bun.lockb',
    '*.min.js', '*.min.css', '*.map', '*_pb2.py', '*_pb2_grpc.py', '*.pb.cc',
    '*.pb.h', '*.generated.*', '*.g.cs', '*.Designer.cs',
)


def exclusions(extra=()):
    patterns = [f'**/{name}/**' for name in EXCLUDED_DIRS]
    patterns += [f'**/{name}' for name in EXCLUDED_FILES]
    return [f':(top,exclude,icase,glob){pattern}' for pattern in (*patterns, *extra)]
