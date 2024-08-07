import subprocess

def run_dataflow(request):
    subprocess.run([
        'python', 'bqscriptv2.py',
        '--input_file', 'input_data.txt',
        '--output_path', 'gs://streamdata_bk/output',
        '--project', 'gdab-430616',
        '--region', 'us-west1',
        '--temp_location', 'gs://streamdata_bk/temp',
        '--runner', 'DataflowRunner'
    ])
    return 'Pipeline started', 200
