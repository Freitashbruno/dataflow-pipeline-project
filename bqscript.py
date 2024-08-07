import argparse
import apache_beam as beam
import logging
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam import window
from datetime import datetime

class AddWindowdtlsFn(beam.DoFn):
    def process(self, element, window=beam.DoFn.WindowParam):
        window_start = window.start.to_utc_datetime()
        window_end = window.end.to_utc_datetime()
        pc = str(element) + '  [ ' + str(window_start) + '  -  ' + str(window_end) + ' ]'
        pc = pc.split('\n')
        return pc

def parse_event(x):
    logging.info(f"Parsing event: {x}")
    if x is None or x.strip() == "":
        logging.warning(f"Encountered empty or None line: {x}")
        return None
    try:
        event_nbr, event_time_str = x.split(':', 1)
        event_time = datetime.strptime(event_time_str.strip(), '%Y-%m-%d %H:%M:%S.%f')
        logging.info(f"Parsed event: event_nbr={event_nbr}, event_time={event_time}")
        return {'event_nbr': event_nbr, 'event_time': event_time}
    except Exception as e:
        logging.error(f"Error parsing line {x}: {e}")
        return None

def run(input_file, output_path, pipeline_args=None):
    # Teste rápido para verificar a leitura do arquivo
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            logging.info(f"File line: {line.strip()}")

    pipeline_options = PipelineOptions(pipeline_args, streaming=False, save_main_session=True)
    with beam.Pipeline(options=pipeline_options) as p:
        raw_events = (
            p
            | "Read Events stream data from File" >> beam.io.ReadFromText(input_file)
            | 'Log Raw Events in Pipeline' >> beam.Map(lambda x: logging.info(f"Pipeline Raw Event: {x}") or x)
        )

        parsed_events = (
            raw_events
            | 'Parse Events Data' >> beam.Map(lambda x: logging.info(f"Event before parse: {x}") or parse_event(x))
        )

        non_none_events = (
            parsed_events
            | 'Filter None Events' >> beam.Filter(lambda x: logging.info(f"Event before filter: {x}") or x is not None)
            | 'Log Parsed Events' >> beam.Map(lambda x: logging.info(f"Parsed Event: {x}") or x)
        )

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", help="Path of the input file.")
    parser.add_argument("--output_path", help="Path of the output GCS file including the prefix.")
    known_args, pipeline_args = parser.parse_known_args()
    run(known_args.input_file, known_args.output_path, pipeline_args)
