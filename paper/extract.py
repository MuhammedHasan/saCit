import subprocess
import settings


def extract_all(paper_text):
    '''Extract all from text file and return string in xml format'''
    proc = subprocess.Popen(
        [
            'docker', 'exec', 'pars',
            'local/parscit/bin/citeExtract.pl',
            '-m', 'extract_all',
            settings.PARSCIT_CONTAINER_DATA_VOLUME_LOCATION_FOR_CONTAINER +
            '/' + _save_into_docker(paper_text)
        ],
        stdout=subprocess.PIPE)

    (output, errors) = proc.communicate()

    if errors:
        raise RuntimeError(errors)

    return output


def _save_into_docker(paper_text):
    paper_file = open(
        settings.PARSCIT_CONTAINER_DATA_VOLUME_LOCATION_FOR_HOST + '/' +
        'paper_text.txt', 'w'
    )
    paper_file.write(paper_text)

    return 'paper_text.txt'
