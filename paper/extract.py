import subprocess
import settings
import uuid
import os


def extract_all(paper_text):
    '''Extract all from text file and return string in xml format'''
    filename = _save_into_docker(paper_text)

    proc = subprocess.Popen(
        [
            'docker', 'exec', 'pars',
            'local/parscit/bin/citeExtract.pl',
            '-m', 'extract_all',
            settings.PARSCIT_CONTAINER_DATA_VOLUME_LOCATION_FOR_CONTAINER +
            '/' + filename + '.txt'
        ],
        stdout=subprocess.PIPE)

    (output, errors) = proc.communicate()

    _delete_files(filename)

    if errors:
        raise RuntimeError(errors)

    return output


def _save_into_docker(paper_text):
    filename = str(uuid.uuid4())
    paper_file = open(
        settings.PARSCIT_CONTAINER_DATA_VOLUME_LOCATION_FOR_HOST + '/' +
        filename + '.txt', 'w'
    )
    paper_file.write(paper_text.encode('utf-8'))
    return filename


def _delete_files(filename):
    filepath = settings.PARSCIT_CONTAINER_DATA_VOLUME_LOCATION_FOR_HOST + '/' + filename
    os.remove(filepath + '.txt')
    os.remove(filepath + '.body')
    os.remove(filepath + '.cite')
