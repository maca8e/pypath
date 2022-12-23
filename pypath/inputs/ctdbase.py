#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#
#  Copyright
#  2014-2022
#  EMBL, EMBL-EBI, Uniklinik RWTH Aachen, Heidelberg University
#
#  Authors: Dénes Türei (turei.denes@gmail.com)
#           Nicolàs Palacio
#           Sebastian Lobentanzer
#           Erva Ulusoy
#           Olga Ivanova
#           Ahmet Rifaioglu
#           Melih Darcan
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.organism/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.organism/
#

from __future__ import annotations

import collections

from pypath.share import curl
from pypath.resources.urls import urls


CTD_URLS = {
    'chemical-gene': 'CTD_chem_gene_ixns.tsv.gz',
    'chemical-disease': 'CTD_chemicals_diseases.tsv.gz',
    'disease-pathway': 'CTD_diseases_pathways.tsv.gz',
    'chemical-phenotype': 'CTD_pheno_term_ixns.tsv.gz',
    'gene-disease': 'CTD_genes_diseases.tsv.gz',
    'chemical-vocabulary': 'CTD_chemicals.tsv.gz',
    'gene-vocabulary': 'CTD_genes.tsv.gz',
    'disease-vocabulary': 'CTD_diseases.tsv.gz',
    'pathway-vocabulary': 'CTD_pathways.tsv.gz',
    'anatomy_vocabulary': 'CTD_anatomy.tsv.gz',
    'phenotype-vocabulary': 'CTD_phenotypes.tsv.gz',
}


def _ctdbase_download(_type: str) -> list[tuple]:
    """
    Retrieves a CTDbase file and returns entries as a list of tuples.
    """

    if '-' not in _type:
        _type = f'{_type}-vocabulary'
    url = urls['ctdbase']['url'] % CTD_URLS[_type]

    c = curl.Curl(
        url,
        silent=False,
        large=True,
        encoding="utf-8",
        default_mode="r",
        compressed=True,
        compr="gz",
    )

    entries = list()
    fieldnames = None

    for line in c.result:

        if line.startswith("#"):

            line = line.strip(" #\n").split("\t")

            if len(line) > 1:
                fieldnames = [fieldname for fieldname in line if fieldname != '']
                record = collections.namedtuple('CTDEntry', fieldnames)

            continue

        data = line.split("\t")

        # if data[-1] == "\n":
        #     del data[-1]

        for i, v in enumerate(data):

            is_list = "|" in v
            has_sublist = "^" in v

            if is_list:
                v = v.split("|")
            
                if has_sublist:
                    v = [element.split("^") for element in v]

            elif has_sublist:
                v = [v.split("^")]

            data[i] = v

        entry = {}
        for (fieldname, element) in zip(fieldnames, data):
            if element != "":
                if type(element) == str:
                    element = element.strip()
                elif type(element) == list:
                    element = [elem.strip() for elem in element if type(elem) == str]
            else:
                element = None
            entry[fieldname] = element

        if _type == 'chemical-phenotype':

            entry_pairs = (
                ('comentionedterms', ['name', 'id', 'source']),
                ('anatomyterms',['sequenceorder', 'name', 'id']),
                ('inferencegenesymbols',['name', 'id']),
                ('interactionactions',['interaction', 'action']),
            )

            relation = _modify_dict(entry, entry_pairs)
        try:
            entries.append(record(**entry))
        except TypeError:
            print(entry)
            raise
        
    return entries


def ctdbase_relations(relation_type: str) -> list[tuple]:
    """
    Retrieves a CTDbase relation file.

    Args:
        relation_type: One of the following:
            'chemical-gene',
            'chemical-disease',
            'disease-pathway',
            'chemical-phenotype',
            'gene-disease',

    Returns:
        Relations as a list of tuples.
    """

    return _ctdbase_download(relation_type)


def ctdbase_vocabulary(vocabulary_type: str) -> list[tuple]:
    """
    Retrieves a CTDbase vocabulary file.

    Args:
        vocabulary_type: One of the following:
            'chemical',
            'gene',
            'disease',
            'pathway',
            'anatomy',
            'phenotype',

    Returns:
        Vocabulary as a list of tuples.
    """

    return _ctdbase_download(vocabulary_type)


def _modify_dict(_dict, *entry_pairs):

    for key, new_keys in entry_pairs:

        _dict[key] = _map_keys(
            new_keys,
            _dict[key]
        )
    
    return _dict


def _map_keys(keys, entry):

    if entry == None:
        return None
    
    result = list()

    for values in entry:

        temp_dict = dict()

        for key, value in zip(keys, values):
            temp_dict[key] = value
        
        result.append(temp_dict)

    return result