import string
from os import path
import traceback

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from opengene.exceptions import UnrecognizedFileFormatError


def load_edi(path_edi):
    with open(path_edi, 'r', encoding='ISO-8859-1') as f:
        edi = f.read()

    # Splits edi into list of str
    raw_str_seq_rec_list = edi.split(';-')[:-1]
    seq_rec_list = []

    for raw_str_seq_rec in raw_str_seq_rec_list:
        # separate name, description and sequence
        str_seq_rec = raw_str_seq_rec.split('\n;')

        try:
            name = str_seq_rec[1][1:]  # We get the name without the trailing whitespace
            str_seq = str_seq_rec[-1]

            # remove \n et whitespaces from Sequence
            str_seq = str_seq.translate({ord(c): None for c in string.whitespace})

            seq_rec = SeqRecord(Seq(str_seq), name=name)
            seq_rec_list.append(seq_rec)

        except IndexError:
            traceback.print_exc()
            raise UnrecognizedFileFormatError(path_edi)

    return seq_rec_list


def load_fasta(path_fasta):
    SeqIO.parse(path_fasta, "fasta")


def load_file(path_file):
    # TODO: Detect file format even without extension + add other file formats
    file_ext = path.splitext(path_file)[1]
    if file_ext == ".fasta" or file_ext == ".fa":
        file_type = "fasta"
    elif file_ext == ".edi" or file_ext == ".adn":
        file_type = "edi"
    else:
        file_type = "unknown"

    if file_type == "fasta":
        return load_fasta(path_file)
    elif file_type == "edi":
        return load_edi(path_file)
    else:
        raise UnrecognizedFileFormatError(path_file)


def write_fasta_file(seq_rec_list, path_fasta):
    SeqIO.write(seq_rec_list, path_fasta, "fasta")


def write_edi_file(seq_rec_list, path_edi):
    pass  # TODO
