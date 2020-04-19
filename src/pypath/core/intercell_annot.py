#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#  Annotation information for intercell.py
#
#  Copyright
#  2014-2020
#  EMBL, EMBL-EBI, Uniklinik RWTH Aachen, Heidelberg University
#
#  File author(s): Dénes Türei (turei.denes@gmail.com)
#                  Nicolàs Palacio
#                  Olga Ivanova
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.org/
#

import importlib as imp

import pypath.utils.go as go
import pypath.inputs.main as dataio
import pypath.internals.annot_formats as af


#TODO should go to jsons
"""
Gene Ontology annotations to select categories relevant in intercellular
signaling.
"""
go_combined_classes = {
    'junction':
        """
        cell junction OR
        cell junction assembly OR
        cell junction organization OR
        intercellular bridge organization OR
        gap junction-mediated intercellular transport OR
        gap junction
        """,
    'gap junction':
        """
        gap junction
        """,
    'tight junction':
        """
        tight junction
        """,
    'cell-substrate junction':
        """
        cell-substrate junction
        """,
    'cell-cell junction':
        """
        cell-cell junction
        """,
    'extracellular':
        """
        extracellular region OR
        extracellular region part
        """,
    'intracellular':
        """
        intracellular organelle OR
        intracellular organelle lumen OR
        intracellular
        """,
    'cell_surface':
        """
        cell surface OR
        external side of plasma membrane
        """,
    'transmembrane':
        """
        integral component of membrane OR
        transmembrane signaling receptor activity
        """,
    'ecm':
        """
        extracellular matrix OR
        complex of collagen trimers OR
        collagen network OR
        banded collagen fibril OR
        collagen beaded filament OR
        elastic fiber OR
        fibronectin fibril
        """,
    'extracell enzyme':
        """
        catalytic activity AND
        extracellular region
        """,
    'enzyme':
        """
        catalytic activity
        """,
    'extracell peptidase':
        """
        peptidase activity AND
        extracellular region
        """,
    'peptidase':
        """
        peptidase activity
        """,
    'growth factor binding':
        """
        growth factor binding AND
        extracellular space
        """,
    'receptor regulation':
        """
        (receptor regulator activity OR
        regulation of receptor recycling OR
        receptor clustering OR
        receptor diffusion trapping OR
        membrane raft localization) AND
        (extracellular region OR
        cell surface OR
        external side of plasma membrane OR
        intrinsic component of plasma membrane)
        """,
    'receptor inhibition':
        """
        receptor inhibitor activity AND
        (extracellular region OR
        cell surface OR
        external side of plasma membrane OR
        intrinsic component of plasma membrane)
        """,
    'receptor activation':
        """
        signaling receptor activator activity AND
        (extracellular region OR
        cell surface OR
        external side of plasma membrane OR
        intrinsic component of plasma membrane)
        """,
    'ligands':
        """
        receptor ligand activity AND
        (extracellular region OR
        cell surface OR
        external side of plasma membrane)
        """,
    'secreted ligands':
        """
        receptor ligand activity AND
        extracellular region
        """,
    'surface ligands':
        """
        receptor ligand activity AND
        (cell surface OR
        external side of plasma membrane)
        """,
    'receptors':
        """
        (signaling receptor activity OR
        cell surface receptor signaling pathway OR
        transmembrane signaling receptor activity OR
        receptor complex OR
        (cellular response to stimulus AND signal transduction)) AND
        (cell surface OR
        external side of plasma membrane)
        """,
    'membrane ligands':
        """
        receptor ligand activity AND
        (cell surface OR
        external side of plasma membrane)
        """,
    'hormone receptors':
        """
        hormone binding AND
        (cell surface OR
        external side of plasma membrane)
        """,
    'ecm structure':
        """
        (extracellular region OR
        extracellular matrix) AND
        (structural molecule activity OR
        extracellular matrix structural constituent OR
        structural constituent of bone)
        """,
    'ecm production':
        """
        extracellular matrix assembly OR
        extracellular matrix organization OR
        extracellular matrix constituent secretion OR
        collagen metabolic process
        """,
    'endocytosis':
        """
        cargo adaptor activity
        """,
    'adhesion to matrix':
        """
        cell adhesion mediator activity OR
        extracellular matrix binding OR
        hydroxyapatite binding OR
        cell-substrate adhesion
        """,
    'response to adhesion':
        """
        cellular response to cell-matrix adhesion OR
        contact inhibition OR
        establishment or maintenance of cell polarity OR
        extracellular matrix-cell signaling
        """,
    'adhesion to other cells':
        """
        cell-cell adhesion
        """,
    'adhesion':
        """
        cell adhesion mediator activity OR
        extracellular matrix binding OR
        hydroxyapatite binding OR
        cell adhesion OR
        cell-cell adhesion OR
        cell-substrate adhesion OR
        cell adhesion molecule production OR
        cell-cell adhesion in response to extracellular stimulus OR
        cellular response to cell-matrix adhesion OR
        contact inhibition OR
        establishment or maintenance of cell polarity
        """,
    'cell-cell signaling':
        """
        cell-cell signaling
        """,
    'transport':
        """
        intrinsic component of plasma membrane AND
        transmembrane transporter activity
        """,
    'regulation of transport':
        """
        (cell surface OR
        external side of plasma membrane OR
        extracellular region) AND
        (regulation of transmembrane transporter activity OR
        channel regulator activity)
        """,
    'ion channels':
        """
        (ion channel activity OR
        ion transmembrane transporter activity) AND
        intrinsic component of plasma membrane
        """,
    'regulation of ion channels':
        """
        (cell surface OR
        external side of plasma membrane OR
        extracellular region) AND
        (ion channel regulator activity OR
        regulation of ion transmembrane transporter activity OR
        channel regulator activity)
        """,
    'autocrine signaling':
        """
        autocrine signaling
        """,
    'paracrine signaling':
        """
        paracrine signaling
        """,
    'signal release':
        """
        signal release OR
        hormone secretion OR
        hormone metabolic process OR
        cytokine production OR
        cytokine secretion
        """,
    'secretion':
        """
        exocytic process OR
        secretion by cell
        """,
    'communication by exosomes':
        """
        extracellular vesicle biogenesis OR
        extracellular exosome assembly OR
        vesicle-mediated intercellular transport OR
        cell-cell signaling via exosome
        """,
    'membrane docking':
        """
        membrane docking AND
        (extracellular region OR
        cell surface OR
        external side of plasma membrane)
        """
}


annotation_categories = [
    ('MatrixDB_Secreted',),
    ('MatrixDB_ECM',),
    ('Surfaceome',),
    ('GO_Intercell', 'adhesion'),
    ('GO_Intercell', 'cell_surface'),
    ('GO_Intercell', 'ecm'),
    ('GO_Intercell', 'ecm structure'),
    ('GO_Intercell', 'extracell enzyme'),
    ('GO_Intercell', 'extracell peptidase'),
    ('GO_Intercell', 'extracellular'),
    ('GO_Intercell', 'hormone receptors'),
    ('GO_Intercell', 'ion channels'),
    ('GO_Intercell', 'junction'),
    ('GO_Intercell', 'ligands'),
    ('GO_Intercell', 'receptors'),
    ('MatrixDB_Membrane',),
    ('Membranome', 'Plasma membrane', 'extracellular side'),
    ('CSPA',),
    ('LOCATE', 'extracellular'),
    ('LOCATE', 'extracellular region'),
    ('LOCATE', 'plasma membrane'),
    ('Matrisome', 'Core matrisome'),
    ('Matrisome', 'Matrisome-associated'),
    ('Matrisome', 'Core matrisome', 'Collagens'),
    ('Matrisome', 'Core matrisome', 'ECM Glycoproteins'),
    ('Matrisome', 'Core matrisome', 'Proteoglycans'),
    ('Matrisome', 'Matrisome-associated', 'ECM Regulators'),
    ('Matrisome', 'Matrisome-associated', 'ECM-affiliated Proteins'),
    ('Matrisome', 'Matrisome-associated', 'Secreted Factors'),
]

[
    ('GO_Intercell', 'adhesion'),
    ('GO_Intercell', 'cell_surface'),
    ('GO_Intercell', 'ecm structure'),
    ('GO_Intercell', 'extracell enzyme'),
    ('GO_Intercell', 'extracell peptidase'),
    ('GO_Intercell', 'ion channels'),
    ('GO_Intercell', 'junction'),
    ('GO_Intercell', 'ligands'),
    ('GO_Intercell', 'receptors'),
]


go_single_terms = {

    # cellular component
    'C': {
        # junction
        'cell junction',

        # extracellular
        'extracellular region',
        'extracellular region part',

        # extracellular_matrix
        'extracellular matrix',
        'complex of collagen trimers',
        'collagen network',
        'banded collagen fibril',
        'collagen beaded filament',
        'elastic fiber',
        'fibronectin fibril',

        # exosome
        # could not find sub-term for their membrane or lumen
        'extracellular vesicle',

        # cell_surface
        # only plasma membrane components facing outside
        'cell surface',
        'external side of plasma membrane',

        # these contains also intracellular components
        'plasma membrane',
        'extrinsic component of plasma membrane',
        'intrinsic component of plasma membrane',
        'cytoplasmic side of plasma membrane',

        'immunological synapse',

        'clathrin-coated pit',
        'plasma membrane raft',

        'presynaptic membrane',
        'presynaptic endocytic zone',
        'presynaptic endocytic zone membrane',
        'intrinsic component of presynaptic membrane',
        'extrinsic component of presynaptic membrane',
        'presynaptic active zone membrane',

        'postsynaptic density membrane',
        'intrinsic component of postsynaptic density membrane',
        'extrinsic component of postsynaptic density membrane',

        'synaptic vesicle',
        'intrinsic component of synaptic vesicle membrane',
        'synaptic vesicle lumen',
        'synaptic vesicle membrane',
        'extracellular matrix of synaptic cleft',

        'axolemma',
        'neuron projection membrane',
        'neuronal cell body membrane',
        'photoreceptor inner segment membrane',
        'photoreceptor outer segment membrane',
        'stereocilium membrane',
        'stereocilia coupling link',

    },

    # molecular function
    'F': {

        # upper level terms which help to categorize
        # molecular functions in the intercellular signaling
        'molecular carrier activity',
        'cargo receptor activity',
        'binding',
        'regulation of binding',
        'positive regulation of binding',
        'negative regulation of binding',
        'protein folding chaperone',
        'antioxidant activity',

        # upper level generic terms for regulation
        'regulation of molecular function',
        'negative regulation of molecular function',
        'positive regulation of molecular function',

        # enzymes
        'catalytic activity',
        'regulation of catalytic activity',
        'positive regulation of catalytic activity',
        'negative regulation of catalytic activity',
        'enzyme regulator activity',
        'enzyme activator activity',
        'enzyme inhibitor activity',
        'catalytic activity, acting on a protein',
        # peptidases
        'peptidase activity',
        'peptidase regulator activity',
        'peptidase activator activity',
        'peptidase inhibitor activity',
        'regulation of peptidase activity',
        'peptidase activator activity',
        # receptors
        'receptor regulator activity',
        'signaling receptor activator activity',
        'receptor inhibitor activity',
        'receptor ligand activity',
        'neurotransmitter receptor regulator activity',
        'signaling receptor activity',
        'negative regulation of signaling receptor activity',
        'positive regulation of signaling receptor activity',
        'signaling receptor activator activity',
        'receptor inhibitor activity',
        'regulation of signaling receptor activity',
        'receptor complex',
        (
            'transforming growth factor beta receptor,'
            'cytoplasmic mediator activity'
        ),
        # other relevant binding activities
        'antigen binding',
        'hormone binding',
        'neurotransmitter binding',

        # endocytosis
        'cargo adaptor activity',

        # ECM, structural proteins
        'structural molecule activity',
        'extracellular matrix structural constituent',
        'structural constituent of bone',

        # adhesion to base membrane and ECM
        'cell adhesion mediator activity',
        'extracellular matrix binding',
        'hydroxyapatite binding',

        # transporters
        'transporter activity',
        'regulation of transporter activity',
        'positive regulation of transporter activity',
        'negative regulation of transporter activity',
        'transmembrane transporter activity',
        'drug transmembrane transporter activity',
        'regulation of transmembrane transporter activity',
        # channels
        'channel regulator activity',
        'channel activator activity',
        'channel inhibitor activity',
        # ion channels
        'ion channel inhibitor activity',
        'ion channel regulator activity',
        'ion transmembrane transporter activity',
        'regulation of ion transmembrane transporter activity',
        'positive regulation of ion transmembrane transporter activity',
        'negative regulation of ion transmembrane transporter activity',
    },

    # biological process
    'P': {

        # cell adhesion
        'cell adhesion',
        'cell-cell adhesion',
        'cell-substrate adhesion',
        'cell adhesion molecule production',
        'cell-cell adhesion in response to extracellular stimulus',
        'cellular response to cell-matrix adhesion',
        'contact inhibition',
        'establishment or maintenance of cell polarity'

        # cellular responses
        'myofibroblast cell apoptotic process',
        'fibroblast apoptotic process',
        'epithelial cell apoptotic process',

        # cell activation
        'cell activation',
        'endothelial cell activation',
        'fibroblast activation',
        'leukocyte activation',

        # cell communication
        'cell communication',
        'cell communication by chemical coupling',
        'cell communication by electrical coupling',
        'cell-cell signaling',
        'autocrine signaling',
        'paracrine signaling',
        'cell-cell signaling via exosome',
        'epithelial-mesenchymal cell signaling',
        'cellular response to extracellular stimulus',
        'synaptic signaling',
        'cell-cell recognition',

        # signal release
        'signal release',
        'hormone secretion',
        'exocytic process',
        'secretion by cell',
        'hormone metabolic process',
        'cytokine production',
        'cytokine secretion',

        # receptors
        'regulation of receptor recycling',
        'receptor clustering',
        'receptor diffusion trapping',
        'membrane raft localization',

        # exosomes
        'extracellular vesicle biogenesis',
        'extracellular exosome assembly',
        'vesicle-mediated intercellular transport',

        # junction
        'cell junction assembly',
        'cell junction organization',
        'intercellular bridge organization',
        'gap junction-mediated intercellular transport',

        # ECM
        'extracellular matrix assembly',
        'extracellular matrix organization',
        'extracellular matrix constituent secretion',
        'extracellular matrix-cell signaling',
        'cell-matrix recognition',
        'collagen metabolic process',

        # motility
        'fibroblast migration',
        'epithelial cell migration',
        'endothelial cell migration',
        'leukocyte migration',
        'substrate-dependent cell migration',
        'cell chemotaxis to fibroblast growth factor',
        'endothelial cell chemotaxis',
        'fibroblast chemotaxis',
        'leukocyte chemotaxis',
        'epithelial structure maintenance',
        'connective tissue replacement', # this is fibrosis actually

        # channels
        'ion channel activity',

        # docking
        'membrane docking',
        'protein to membrane docking',
        'membrane to membrane docking',

        # kidney specific stuff
        'nephron',
        'outer medulla of kidney',
        'inner medulla of kidney',
        'kidney pyramid',

    },

}


"""
Higher level classes of intercellular communication roles.
"""
annot_combined_classes = (
    af.AnnotDef(
        name = 'adaptor_adhesome',
        source = 'Adhesome',
        args = {'mainclass': 'Adaptor'},
    ),
    af.AnnotDef(
        name = 'channel_adhesome',
        source = 'Adhesome',
        args = {'mainclass': 'Channel'},
    ),
    af.AnnotDef(
        name = 'actin_regulation_adhesome',
        source = 'Adhesome',
        args = {'mainclass': 'Actin regulation'},
    ),
    af.AnnotDef(
        name = 'adhesion_receptor_adhesome',
        source = 'Adhesome',
        args = {'mainclass': 'Adhesion receptor'},
    ),
    # receptor
    af.AnnotDef(
        name = 'receptor',
        source = af.AnnotOp(
            annots = (
                'receptor_cellphonedb',
                'receptor_surfaceome',
                'receptor_go',
                'receptor_hpmr',
                'receptor_ramilowski',
                'receptor_kirouac',
                'receptor_guide2pharma',
                'receptor_hgnc',
                'receptor_dgidb',
                'receptor_baccin',
                'receptor_signalink',
                'receptor_embrace',
                'receptor_italk',
                'receptor_cellcellinteractions',
                'receptor_almen',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'receptor_italk',
        source = 'iTALK',
        args = {
            'mainclass': 'receptor',
        },
    ),
    af.AnnotDef(
        name = 'receptor_almen',
        source = 'Almen2009',
        args = {
            'mainclass': 'Receptors',
        },
    ),
    af.AnnotDef(
        name = 'receptor_cellcellinteractions',
        source = 'CellCellInteractions',
        args = {
            'mainclass': 'Receptor',
        },
    ),
    af.AnnotDef(
        name = 'receptor_embrace',
        source = 'EMBRACE',
        args = {
            'mainclass': 'receptor',
        },
    ),
    af.AnnotDef(
        name = 'receptor_hgnc',
        source = af.AnnotOp(
            annots = (
                'interleukin_receptor_hgnc',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'interleukin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interleukin receptors',
        },
    ),
    af.AnnotDef(
        name = 'receptor_cellphonedb',
        source = 'CellPhoneDB',
        args = {
            'receptor': bool,
            'transmembrane': True,
        },
    ),
    af.AnnotDef(
        name = 'receptor_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'receptors',
        },
    ),
    af.AnnotDef(
        name = 'receptor_hpmr',
        source = 'HPMR',
        args = {
            'role': 'Receptor',
        },
    ),
    af.AnnotDef(
        name = 'receptor_surfaceome',
        source = 'Surfaceome',
        args = {
            'mainclass': 'Receptors',
        },
    ),
    af.AnnotDef(
        name = 'receptor_ramilowski',
        source = 'Ramilowski2015',
        args = {
            'mainclass': 'receptor',
        },
    ),
    af.AnnotDef(
        name = 'receptor_kirouac',
        source = 'Kirouac2010',
        args = {
            'mainclass': 'receptor',
        },
    ),
    af.AnnotDef(
        name = 'receptor_guide2pharma',
        source = 'Guide2Pharma',
        args = {
            'mainclass': 'receptor',
        },
    ),
    af.AnnotDef(
        name = 'receptor_dgidb',
        source = 'DGIdb',
        args = {
            'category': 'G PROTEIN COUPLED RECEPTOR',
        },
    ),
    af.AnnotDef(
        name = 'receptor_lrdb',
        source = 'LRdb',
        args = {
            'role': 'receptor',
            'references': bool,
        },
    ),
    af.AnnotDef(
        name = 'receptor_baccin',
        source = 'Baccin2019',
        args = {
            'mainclass': 'receptor',
        },
    ),
    af.AnnotDef(
        name = 'receptor_signalink',
        source = 'SignaLink_function',
        args = {
            'function': 'Receptor',
        },
    ),
    # receptor subclasses from HGNC
    af.AnnotDef(
        name = 'immunoglobulin_like_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Activating leukocyte immunoglobulin like receptors',
        },
    ),
    af.AnnotDef(
        name = 'adiponectin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Adiponectin receptors',
        },
    ),
    af.AnnotDef(
        name = 'adrenalin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Adrenoceptors',
        },
    ),
    af.AnnotDef(
        name = 'angiotensin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Angiotensin receptors',
        },
    ),
    af.AnnotDef(
        name = 'vasopressin_oxytocin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Arginine vasopressin and oxytocin receptors',
        },
    ),
    af.AnnotDef(
        name = 'atypical_chemokine_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Atypical chemokine receptors',
        },
    ),
    af.AnnotDef(
        name = 'basigin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Basigin family',
        },
    ),
    af.AnnotDef(
        name = 'bombesin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Bombesin receptors',
        },
    ),
    af.AnnotDef(
        name = 'bradykinin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Bradykinin receptors',
        },
    ),
    af.AnnotDef(
        name = 'butyrophilin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Butyrophilins',
        },
    ),
    af.AnnotDef(
        name = 'cc_chemokine_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'C-C motif chemokine receptors',
        },
    ),
    af.AnnotDef(
        name = 'cx3c_chemokine_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'C-X-3-C motif chemokine receptors',
        },
    ),
    af.AnnotDef(
        name = 'cxc_chemokine_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'C-X-C motif chemokine receptors',
        },
    ),
    af.AnnotDef(
        name = 'celsr_cadherin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'CELSR cadherins',
        },
    ),
    af.AnnotDef(
        name = '5ht_gprotein_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': '5-hydroxytryptamine receptors, G protein-coupled',
        },
    ),
    af.AnnotDef(
        name = '5ht_ionotropic_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': '5-hydroxytryptamine receptors, ionotropic',
        },
    ),
    af.AnnotDef(
        name = 'activating_leukocyte_ig_like_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Activating leukocyte immunoglobulin like receptors',
        },
    ),
    af.AnnotDef(
        name = 'adenosine_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Adenosine receptors',
        },
    ),
    af.AnnotDef(
        name = 'calcitonin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Calcitonin receptors',
        },
    ),
    af.AnnotDef(
        name = 'calcium_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Calcium sensing receptors',
        },
    ),
    af.AnnotDef(
        name = 'cannabinoid_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cannabinoid receptors',
        },
    ),
    af.AnnotDef(
        name = 'chemerin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Chemerin receptor',
        },
    ),
    af.AnnotDef(
        name = 'cholecystokinin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cholecystokinin receptors',
        },
    ),
    af.AnnotDef(
        name = 'muscarinic_cholinergic_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cholinergic receptors muscarinic',
        },
    ),
    af.AnnotDef(
        name = 'nicotinic_cholinergic_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cholinergic receptors nicotinic subunits',
        },
    ),
    af.AnnotDef(
        name = 'collectin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Collectins',
        },
    ), # innate immunity receptors for sugar and lipid patterns
    af.AnnotDef(
        name = 'complement_gpcr_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Complement component GPCRs',
        },
    ), # receptors for chemotactic immune signals
    af.AnnotDef(
        name = 'crh_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Corticotropin releasing hormone receptors',
        },
    ),
    af.AnnotDef(
        name = 'dopamine_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Dopamine receptors',
        },
    ),
    af.AnnotDef(
        name = 'ephrin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'EPH receptors',
        },
    ),
    af.AnnotDef(
        name = 'endothelin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Endothelin receptors',
        },
    ),
    af.AnnotDef(
        name = 'erbb_rtk_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Erb-b2 receptor tyrosine kinases',
        },
    ),
    af.AnnotDef(
        name = 'f2r_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'F2R receptors',
        },
    ), # GPCRs for thrombin and trypsin
    af.AnnotDef(
        name = 'formyl_peptide_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Formyl peptide receptors',
        },
    ), # formyl-methionyl peptides are neutrophil chemoattractants
    af.AnnotDef(
        name = 'free_fatty_acid_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Free fatty acid receptors',
        },
    ),  # intestinal short chain fatty acid GPCRs, regulating
        # whole-body energy homeostasis
    af.AnnotDef(
        name = 'bile_acid_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'G protein-coupled bile acid receptor',
        },
    ),  # GPCR for bile acid
    af.AnnotDef(
        name = 'estrogen_gpcr_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'G protein-coupled estrogen receptor',
        },
    ),  # although this receptor is intracellular, there is no reason we
        # shouldn't treat it the same way as plasma membrane receptors
    af.AnnotDef(
        name = 'gpcr_orphan_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': {
                'G protein-coupled receptors, Class A orphans',
                'G protein-coupled receptors, Class C orphans',
            },
        },
    ),  # GPCRs mostly without known ligand, all in the cell membrane
    af.AnnotDef(
        name = 'frizzled_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'G protein-coupled receptors, Class F frizzled',
        },
    ),  # GPCRs for Wnt
    af.AnnotDef(
        name = 'galanin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Galanin receptors',
        },
    ),
    af.AnnotDef(
        name = 'gaba_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': {
                'Gamma-aminobutyric acid type A receptor subunits',
                'Gamma-aminobutyric acid type B receptor subunits',
            }
        },
    ),
    af.AnnotDef(
        name = 'glucagon_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Glucagon receptor family',
        },
    ),
    af.AnnotDef(
        name = 'glutamate_ionotropic_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': {
                'Glutamate ionotropic receptor AMPA type subunits',
                'Glutamate ionotropic receptor NMDA type subunits',
                'Glutamate ionotropic receptor delta type subunits',
                'Glutamate ionotropic receptor kainate type subunits',
            }
        },
    ),
    af.AnnotDef(
        name = 'glutamate_metabotropic_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Glutamate metabotropic receptors',
        },
    ),
    af.AnnotDef(
        name = 'glycine_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Glycine receptors',
        },
    ),
    af.AnnotDef(
        name = 'glycoprotein_hormone_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Glycoprotein hormone receptors',
        },
    ),  # receptors for TSH, FSH and LH
    af.AnnotDef(
        name = 'gonadotropin_releasing_hormone_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Gonadotropin releasing hormone receptors',
        },
    ),  # receptors for GnRH
    af.AnnotDef(
        name = 'natriuretic_peptide_receptor_omnipath',
        source = {'P16066', 'P20594'},
    ),
    af.AnnotDef(
        name = 'guanilyn_receptor_omnipath',
        source = {'P25092'},
    ),
    af.AnnotDef(
        name = 'histamine_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Histamine receptors',
        },
    ),
    af.AnnotDef(
        name = 'hydroxycarboxylic_acid_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Hydroxy-carboxylic acid receptors',
        },
    ),  # receptors for lactate, niacin, etc
    af.AnnotDef(
        name = 'orexin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Hypocretin receptors',
        },
    ),
    af.AnnotDef(
        name = 'inhibitory_leukocyte_ig_like_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Inhibitory leukocyte immunoglobulin like receptors',
        },
    ),
    af.AnnotDef(
        name = 'interferon_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interferon receptors',
        },
    ),
    af.AnnotDef(
        name = 'interleukin_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interleukin receptors',
        },
    ),
    af.AnnotDef(
        name = 'killer_cell_ig_like_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Killer cell immunoglobulin like receptors',
        },
    ),  # receptors for HLAs
    af.AnnotDef(
        name = 'killer_cell_lectin_like_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Killer cell lectin like receptors',
        },
    ),  # receptors mostly for HLAs

    # ECM
    af.AnnotDef(
        name = 'ecm',
        source = af.AnnotOp(
            annots = (
                'ecm_matrixdb',
                'ecm_matrisome',
                'ecm_go',
                'ecm_ramilowski',
                'ecm_cellcellinteractions',
                'ecm_uniprot',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'ecm_matrisome',
        source = af.AnnotOp(
            annots = (
                af.AnnotDef(
                    name = 'ecm_matrisome_core',
                    source = 'Matrisome',
                    args = {
                        'mainclass': 'Core matrisome',
                    },
                ),
                af.AnnotOp(
                    annots = (
                        af.AnnotDef(
                            name = 'ecm_matrisome_affiliated',
                            source = 'Matrisome',
                            args = {
                                'mainclass': 'Matrisome-associated',
                                'subclass': 'ECM-affiliated Proteins',
                            },
                        ),
                        'cell_surface',
                    ),
                    op = set.difference,
                ),
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'ecm_matrixdb',
        source = 'MatrixDB',
        args = {
            'mainclass': 'ecm',
        },
    ),
    af.AnnotDef(
        name = 'ecm_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'ecm structure',
        },
    ),
    af.AnnotDef(
        name = 'ecm_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': {
                'extracellular matrix',
                'basement membrane',
            },
        },
    ),
    af.AnnotDef(
        name = 'ecm_uniprot',
        source = 'UniProt_location',
        args = {
            'location': 'Extracellular matrix',
        },
    ),
    # specific subclasses from HGNC
    af.AnnotDef(
        name = 'collagen_proteoglycan_ecm_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Collagen proteoglycans',
        },
    ),
    af.AnnotDef(
        name = 'collagen_ecm_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Collagens',
        },
    ),
    af.AnnotDef(
        name = 'emi_ecm_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'EMI domain containing',
        },
    ),  # this could be also cell-matrix adhesion, although these proteins
        # are not in the cell membrane but all secreted
    af.AnnotDef(
        name = 'fibrillin_ecm_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Fibrillins',
        },
    ),
    af.AnnotDef(
        name = 'fibulin_ecm_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Fibulins',
        },
    ),  # parts of ECM, especially elastic fibers, one of them is a ligand
        # for EGFR (but still an EVM protein at the same time)
    af.AnnotDef(
        name = 'hyalectan_proteoglycan_ecm_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Hyalectan proteoglycans',
        },
    ),
    af.AnnotDef(
        name = 'ecm_cellcellinteractions',
        source = 'CellCellInteractions',
        args = {
            'mainclass': 'ECM',
        },
    ),

    # ligand
    af.AnnotDef(
        name = 'ligand',
        source = af.AnnotOp(
            annots = (
                'ligand_cellphonedb',
                'ligand_go',
                'ligand_hpmr',
                'ligand_ramilowski',
                'ligand_kirouac',
                'ligand_guide2pharma',
                'ligand_hgnc',
                'ligand_dgidb',
                'ligand_baccin',
                'ligand_signalink',
                'ligand_italk',
                'ligand_cellcellinteractions',
                'ligand_embrace',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'ligand_italk',
        source = 'iTALK',
        args = {
            'mainclass': 'ligand',
        },
    ),
    af.AnnotDef(
        name = 'ligand_cellcellinteractions',
        source = 'CellCellInteractions',
        args = {
            'mainclass': 'Ligand',
        },
    ),
    af.AnnotDef(
        name = 'ligand_embrace',
        source = 'EMBRACE',
        args = {
            'mainclass': 'ligand',
        },
    ),
    af.AnnotDef(
        name = 'ligand_hgnc',
        source = af.AnnotOp(
            annots = (
                'interleukin_hgnc',
                'endogenous_ligand_hgnc',
                'chemokine_ligand_hgnc',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'ligand_cellphonedb',
        source = 'CellPhoneDB',
        args = {
            'secreted': bool,
        },
    ),
    af.AnnotDef(
        name = 'ligand_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'ligands',
        },
    ),
    af.AnnotDef(
        name = 'ligand_hpmr',
        source = 'HPMR',
        args = {
            'role': 'Ligand',
        },
    ),
    af.AnnotDef(
        name = 'ligand_ramilowski',
        source = 'Ramilowski2015',
        args = {
            'mainclass': 'ligand',
        },
    ),
    af.AnnotDef(
        name = 'ligand_kirouac',
        source = 'Kirouac2010',
        args = {
            'mainclass': 'ligand',
        },
    ),
    af.AnnotDef(
        name = 'ligand_guide2pharma',
        source = 'Guide2Pharma',
        args = {
            'mainclass': 'ligand',
        },
    ),
    af.AnnotDef(
        name = 'ligand_dgidb',
        source = af.AnnotOp(
            annots = (
                'growth_factor_dgidb',
                'hormone_dgidb',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'growth_factor_dgidb',
        source = 'DGIdb',
        args = {
            'category': 'GROWTH FACTOR',
        },
    ),
    af.AnnotDef(
        'hormone_dgidb',
        source = 'DGIdb',
        args = {
            'category': 'HORMONE ACTIVITY',
        },
    ),
    af.AnnotDef(
        name = 'ligand_lrdb',
        source = 'LRdb',
        args = {
            'role': 'ligand',
            'references': bool,
        },
    ),
    af.AnnotDef(
        name = 'ligand_baccin',
        source = 'Baccin2019',
        args = {
            'mainclass': 'ligand',
        },
    ),
    af.AnnotDef(
        name = 'ligand_signalink',
        source = 'SignaLink_function',
        args = {
            'function': 'Ligand',
        },
    ),
    # ligands from HGNC
    af.AnnotDef(
        name = 'angiopoietin_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Angiopoietin like family',
        },
    ),
    af.AnnotDef(
        name = 'basigin_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Basigin family',
        },
    ),
    af.AnnotDef(
        name = 'bmp_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Bone morphogenetic proteins',
        },
    ),
    af.AnnotDef(
        name = 'c1q_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'C1q and TNF related',
        },
    ),
    af.AnnotDef(
        name = 'ccn_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cellular communication network factors',
        },
    ),
    af.AnnotDef(
        name = 'interleukin_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interleukins',
        },
    ),
    af.AnnotDef(
        name = 'endogenous_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Endogenous ligands',
        },
    ), # a very few among these are actually not secreted
    af.AnnotDef(
        name = 'chemokine_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Chemokine ligands',
        },
    ),
    af.AnnotDef(
        name = 'neurotrophin_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Neurotrophins',
        },
    ),
    af.AnnotDef(
        name = 'gdnf_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'GDNF family ligands',
        },
    ),
    af.AnnotDef(
        name = 'chordin_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Chordin family',
        },
    ), # BMP antagonist ligands
    af.AnnotDef(
        name = 'cysteine_rich_bmp_regulator_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cysteine rich transmembrane BMP regulators',
        },
    ), # BMP agonist and antagonist ligands
    af.AnnotDef(
        name = 'dan_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'DAN family',
        },
    ), # TGF & BMP signaling agonists and antagonists
    af.AnnotDef(
        name = 'fgf_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Fibroblast growth factor family',
        },
    ), # with the exception of FGF13: that's not secreted
    af.AnnotDef(
        name = 'gdnf_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'GDNF family ligands',
        },
    ), # neurotrophic ligands
    af.AnnotDef(
        name = 'growth_hormone_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Growth hormone family',
        },
    ),
    af.AnnotDef(
        name = 'hedgehog_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Hedgehog signaling molecule family',
        },
    ),  # hedgehog proteins are initially membrane bound and can be
        # solubilized later
    af.AnnotDef(
        name = 'hdgf_ligand_omnipath',
        source = {'P51858'},
    ),  # hepatoma-derived growth factor (HDGFL1 is not included because
        # little is known about its role and whether it's secreted)
    af.AnnotDef(
        name = 'igf_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'IGF like family',
        },
    ),
    af.AnnotDef(
        name = 'izumo_ligand_omnipath',
        source = {'Q1ZYL8'},
    ),  # ligands in sperm-egg fusion
    af.AnnotDef(
        name = 'inhibin_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Inhibin subunits',
        },
    ),
    af.AnnotDef(
        name = 'interleukin6_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interleukin 6 type cytokine family',
        },
    ),
    af.AnnotDef(
        name = 'interleukin_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interleukins',
        },
    ),
    af.AnnotDef(
        name = 'leucine_rich_glioma_inactivated_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'LGI family',
        },
    ),  # maybe not ligands in a strict sense but don't fit either
        # in other categories

    # intracellular
    af.AnnotDef(
        name = 'intracellular',
        source = af.AnnotOp(
            annots = (
                'intracellular_locate',
                'intracellular_comppi',
                'intracellular_go',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'intracellular_locate',
        source = af.AnnotOp(
            annots = (
                af.AnnotDef(
                    name = 'locate_intracellular',
                    source = 'LOCATE',
                    args = {
                        'location': {
                            'centrosome',
                            'cytoplasm',
                            'endosomes',
                            'lysosomes',
                            'nucleus',
                            'plasma membrane',
                            'cytoplasmic membrane-bound vesicle',
                            'cytoplasmic vesicles',
                            'cytoskeleton',
                            'early endosomes',
                            'endoplasmic reticulum',
                            'golgi apparatus',
                            'er-golgi intermediate compartment',
                            'ergic',
                            'golgi cis cisterna',
                            'golgi medial cisterna',
                            'golgi trans cisterna',
                            'golgi trans face',
                            'inner mitochondrial membrane',
                            'late endosomes',
                            'lipid particles',
                            'medial-golgi',
                            'melanosome',
                            'microtubule',
                            'microtubule organizing center ',
                            'mitochondria',
                            'mitochondrial inner membrane',
                            'mitochondrial outer membrane',
                            'mitochondrion',
                            'nuclear envelope',
                            'nucleolus',
                            'nuclear speck',
                            'outer mitochondrial membrane',
                            'peroxisome',
                            'peroxisomes',
                            'sarcolemma',
                            'transport vesicle',
                        },
                    },
                ),
                af.AnnotDef(
                    name = 'locate_cytoplasmic',
                    source = 'LOCATE',
                    args = {
                        'cls': 'cytoplasmic',
                    },
                ),
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'intracellular_comppi',
        source = 'ComPPI',
        args = {
            'location': {
                'cytosol',
                'nucleus',
                'mitochondrion',
            },
        },
    ),
    af.AnnotDef(
        name = 'intracellular_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'intracellular',
        },
    ),

    # extracellular
    af.AnnotDef(
        name = 'extracellular',
        source = af.AnnotOp(
            annots = (
                'extracellular_locate',
                'extracellular_surfaceome',
                'extracellular_matrixdb',
                'extracellular_membranome',
                'extracellular_cspa',
                'extracellular_hpmr',
                'extracellular_cellphonedb',
                'extracellular_hpa',
                'extracellular_uniprot',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'extracellular_locate',
        source = af.AnnotOp(
            annots = (
                af.AnnotDef(
                    name = 'locate_extracellular',
                    source = 'LOCATE',
                    args = {
                        'location': {
                            'extracellular',
                            'extracellular region',
                        },
                    },
                ),
                'secreted_locate',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'extracellular_comppi',
        source = 'ComPPI',
        args = {
            'location': 'extracellular',
        },
    ),
    af.AnnotDef(
        name = 'extracellular_surfaceome',
        source = 'Surfaceome',
    ),
    af.AnnotDef(
        name = 'extracellular_matrixdb',
        source = 'MatrixDB',
        args = {
            'mainclass': {
                'secreted',
                'ecm',
            },
        },
    ),
    af.AnnotDef(
        name = 'extracellular_cspa',
        source = 'CSPA',
    ),
    af.AnnotDef(
        name = 'extracellular_membranome',
        source = 'Membranome',
        args = {
            'membrane': 'Plasma membrane',
            'side': 'extracellular side',
        },
    ),
    af.AnnotDef(
        name = 'extracellular_cellphonedb',
        source = 'CellPhoneDB',
        args = {
            'secreted': bool,
        },
    ),
    af.AnnotDef(
        name = 'extracellular_hpmr',
        source = 'HPMR',
    ),
    af.AnnotDef(
        name = 'extracellular_membranome',
        source = 'Membranome',
        args = {
            'membrane': 'Plasma membrane',
            'side': 'extracellular side',
        },
    ),
    af.AnnotDef(
        name = 'extracellular_hpa',
        source = 'HPA_secretome',
        args = {
            'secreted': bool,
        },
    ),
    af.AnnotDef(
        name = 'extracellular_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': {
                'secreted',
            },
        },
    ),
    af.AnnotDef(
        name = 'extracellular_uniprot',
        source = 'UniProt_location',
        args = {
            'location': {
                'Secreted',
            },
        },
    ),
    # specific subclasses from HGNC
    af.AnnotDef(
        name = 'histatin_extracellular_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Histatins and statherin',
        },
    ),  # secreted into saliva
    af.AnnotDef(
        name = 'iglon5_extracellular_omnipath',
        source = {'A6NGN9'},
    ),  # function is not clear for me
    af.AnnotDef(
        name = 'immunoglobulin_heavy_extracellular_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Immunoglobulin heavy locus at 14q32.33',
        },
    ),  # immunoglobulin heavy chain
    af.AnnotDef(
        name = 'immunoglobulin_kappa_extracellular_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Immunoglobulin kappa locus at 2p11.2',
        },
    ),  # immunoglobulin V region
    af.AnnotDef(
        name = 'immunoglobulin_lambda_extracellular_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Immunoglobulin lambda locus at 22q11.2',
        },
    ),  # immunoglobulin V region

    # cell surface
    af.AnnotDef(
        name = 'cell_surface',
        source = af.AnnotOp(
            annots = (
                'cell_surface_surfaceome',
                'cell_surface_go',
                'cell_surface_hpmr',
                'cell_surface_membranome',
                'cell_surface_cspa',
                'cell_surface_cellphonedb',
                'cell_surface_dgidb',
                'cell_surface_ramilowski',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'cell_surface_hpmr',
        source = 'HPMR',
        args = {
            'role': 'Receptor',
        },
    ),
    af.AnnotDef(
        name = 'cell_surface_surfaceome',
        source = 'Surfaceome',
    ),
    af.AnnotDef(
        name = 'cell_surface_cspa',
        source = 'CSPA',
    ),
    af.AnnotDef(
        name = 'cell_surface_cellphonedb',
        source = 'CellPhoneDB',
        args = {
            'method': lambda a: a.peripheral or a.transmembrane,
        },
    ),
    af.AnnotDef(
        name = 'cell_surface_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'cell_surface',
        },
    ),
    af.AnnotDef(
        name = 'cell_surface_membranome',
        source = 'Membranome',
        args = {
            'membrane': 'Plasma membrane',
            'side': 'extracellular side',
        },
    ),
    af.AnnotDef(
        name = 'cell_surface_dgidb',
        source = 'DGIdb',
        args = {
            'category': {'CELL SURFACE', 'EXTERNAL SIDE OF PLASMA MEMBRANE'},
        },
    ),
    af.AnnotDef(
        name = 'cell_surface_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'cell surface',
        },
    ),
    # specific subclasses from HGNC
    af.AnnotDef(
        name = 'glypican_cell_surface_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Glypicans',
        },
    ),
    af.AnnotDef(
        name = 'immunoglobulin_heavy_cell_surface_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Immunoglobulin heavy locus at 14q32.33',
        },
    ),  # immunoglobulin heavy chain
    af.AnnotDef(
        name = 'immunoglobulin_kappa_cell_surface_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Immunoglobulin kappa locus at 2p11.2',
        },
    ),  # immunoglobulin V region
    af.AnnotDef(
        name = 'immunoglobulin_lambda_cell_surface_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Immunoglobulin lambda locus at 22q11.2',
        },
    ),  # immunoglobulin V region
    af.AnnotDef(
        name = 'ifn_induced_cell_surface_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interferon induced transmembrane proteins',
        },
    ),
    af.AnnotDef(
        name = 'ifn_induced_endocytosis_exocytosis_regulator_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interferon induced transmembrane proteins',
        },
    ),

    # plasma membrane
    af.AnnotDef(
        name = 'plasma_membrane',
        source = af.AnnotOp(
            annots = (
                'transmembrane_cellphonedb',
                'lhfpl_plasma_membrane_hgnc',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'lhfpl_plasma_membrane_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'LHFPL tetraspan proteins',
        }
    ),

    # transmembrane
    af.AnnotDef(
        name = 'transmembrane',
        source = af.AnnotOp(
            annots = (
                'transmembrane_cellphonedb',
                'transmembrane_go',
                'transmembrane_opm',
                'transmembrane_locate',
                'transmembrane_topdb',
                'transmembrane_ramilowski',
                'transmembrane_almen',
                'transmembrane_uniprot',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'transmembrane_almen',
        source = af.AnnotOp(
            annots = (
                'transmembrane_phobius_almen',
                'transmembrane_sosui_almen',
                'transmembrane_tmhmm_almen',
            ),
            op = set.union
        ),
    ),
    af.AnnotDef(
        name = 'transmembrane_phobius_almen',
        source = 'Almen2009',
        args = {
            'transmembrane_phobius': True,
        },
    ),
    af.AnnotDef(
        name = 'transmembrane_sosui_almen',
        source = 'Almen2009',
        args = {
            'transmembrane_sosui': True,
        },
    ),
    af.AnnotDef(
        name = 'transmembrane_tmhmm_almen',
        source = 'Almen2009',
        args = {
            'transmembrane_tmhmm': True,
        },
    ),
    af.AnnotDef(
        name = 'transmembrane_uniprot',
        source = af.AnnotOp(
            annots = (
                af.AnnotDef(
                    name = 'transmembrane_uniprot_location',
                    source = 'UniProt_location',
                    args = {
                        'features': {
                            'Multi-pass membrane protein',
                            'Single-pass membrane protein',
                            'Single-pass type I membrane protein',
                            'Single-pass type II membrane protein',
                            'Single-pass type III membrane protein',
                            'Single-pass type IV membrane protein',
                        },
                    },
                ),
                af.AnnotDef(
                    name = 'transmembrane_uniprot_topology',
                    source = 'UniProt_topology',
                    args = {
                        'topology': 'Transmembrane',
                    },
                ),
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'transmembrane_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'transmembrane',
        },
    ),
    af.AnnotDef(
        name = 'transmembrane_cellphonedb',
        source = 'CellPhoneDB',
        args = {
            'transmembrane': True,
        },
    ),
    af.AnnotDef(
        name = 'transmembrane_opm',
        source = 'OPM',
        args = {
            'transmembrane': True,
        },
    ),
    af.AnnotDef(
        name = 'transmembrane_topdb',
        source = 'TopDB',
        args = {
            'topology': 'Membrane',
        },
    ),
    af.AnnotDef(
        name = 'transmembrane_locate',
        source = 'LOCATE',
        args = {
            'cls': {
                'typeI',
                'typeII',
                'mtmp',
            },
        },
    ),
    af.AnnotDef(
        name = 'transmembrane_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'tmh': bool,
        },
    ),
    af.AnnotDef(
        name = 'lhfpl_transmembrane_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'LHFPL tetraspan proteins',
        }
    ),

    # adhesion
    af.AnnotDef(
        name = 'adhesion',
        source = af.AnnotOp(
            annots = (
                'adhesion_cellphonedb',
                'adhesion_go',
                'adhesion_matrisome',
                'adhesion_hgnc',
                'adhesion_integrins',
                'adhesion_zhong2015',
                'adhesion_adhesome',
                'focal_adhesion_ramilowski',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'adhesion_cellphonedb',
        source = 'CellPhoneDB',
        args = {
            'integrin': bool,
        },
    ),
    af.AnnotDef(
        name = 'adhesion_integrins',
        source = 'Integrins',
    ),
    af.AnnotDef(
        name = 'adhesion_zhong2015',
        source = 'Zhong2015',
    ),
    af.AnnotDef(
        name = 'adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': {
                'Type I classical cadherins',
                'Type II classical cadherins',
                '7D cadherins',
                'Desmosomal cadherins',
                'CELSR cadherins',
                'Clustered protocadherins',
                'Non-clustered protocadherins',
                'Cadherin related',
                'Integrin beta subunits',
                'Integrin alpha subunits',
                'Sialic acid binding Ig like lectins',
                'IgLON cell adhesion molecules',
                'IgCAM CXADR-related subfamily',
                'Nectins and nectin-like molecules',
                'Neurexins',
                'Neuroligins',
                (
                    'Carcinoemryonic antigen related '
                    'cell adhesion molecule family'
                ),
            }
        },
    ),
    af.AnnotDef(
        name = 'adhesion_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': {'adhesion to matrix', 'adhesion to other cells'},
        }
    ),
    af.AnnotDef(
        name = 'adhesion_matrisome',
        source = af.AnnotOp(
            annots = (
                af.AnnotDef(
                    name = 'ecm_affiliated_matrisome',
                    source = 'Matrisome',
                    args = {
                        'mainclass': 'Matrisome-associated',
                        'subclass': 'ECM-affiliated Proteins',
                    },
                ),
                'cell_surface',
            ),
            op = set.intersection,
        ),
    ),
    af.AnnotDef(
        name = 'adhesion_adhesome',
        source = af.AnnotOp(
            annots = (
                'adhesion_receptor_adhesome',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'focal_adhesion_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'focal adhesion',
        },
    ),
    af.AnnotDef(
        name = 'adhesion_gprotein_coupled_receptor_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': {
                'Adhesion G protein-coupled receptors, subfamily A',
                'Adhesion G protein-coupled receptors, subfamily B',
                'Adhesion G protein-coupled receptors, subfamily C',
                'Adhesion G protein-coupled receptors, subfamily D',
                'Adhesion G protein-coupled receptors, subfamily E',
                'Adhesion G protein-coupled receptors, subfamily F',
                'Adhesion G protein-coupled receptors, subfamily G',
                'Adhesion G protein-coupled receptors, subfamily L',
                'Adhesion G protein-coupled receptors, subfamily V',
            },
        }, # cell-matrix adhesion
    ),
    af.AnnotDef(
        name = '7d_cadherin_cell_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': '7D cadherins',
        },
    ), # cell-cell adhesion
    af.AnnotDef(
        name = 'cadherin_related_cell_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cadherin related',
        },
    ), # cell-cell adhesion
    af.AnnotDef(
        name = 'ceacam_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': (
                'Carcinoembryonic antigen related '
                'cell adhesion molecule family'
            ),
        },
    ), # in plasma membrane; cell-cell adhesion and receptors
    af.AnnotDef(
        name = 'clarin_cell_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Clarins',
        },
    ),  # regulation of cell-cell adhesion and synapsis in ear and retina
    af.AnnotDef(
        name = 'protocadherin_cell_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Clustered protocadherins',
        },
    ),  # cell-cell adhesion in brain neuronal connections
    af.AnnotDef(
        name = 'ig_like_cell_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Ig-like cell adhesion molecule family',
        },
        exclude = {'Q9HCN6', 'Q14CZ8'},
    ),
    af.AnnotDef(
        name = 'matrix_adhesion_omnipath',
        source = {'Q9HCN6', 'Q14CZ8'},
    ),
    af.AnnotDef(
        name = 'igcam_cxadr_like_cell_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'IgCAM CXADR-related subfamily',
        },
    ),
    af.AnnotDef(
        name = 'iglon_cell_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'IgLON cell adhesion molecules',
        },
        exclude = {'A6NGN9'},
    ),
    af.AnnotDef(
        name = 'integrin_cell_adhesion_omnipath',
        source = {
            'P23229', 'Q13349', 'Q13797', 'P20701', 'P38570', 'P05107',
            'P26010',
        },
    ),
    af.AnnotDef(
        name = 'integrin_matrix_adhesion_omnipath',
        source = {
            'P06756', 'Q9UKX5', 'P08648', 'P11215', 'P26006', 'Q13683',
            'P20702', 'O75578', 'P13612', 'P17301', 'P56199', 'P08514',
            'P18564', 'O95965', 'P18084', 'P05556', 'P26012', 'P16144',
            'P05106',
        },
    ),

    # surface enzyme
    af.AnnotDef(
        name = 'surface_enzyme',
        source = af.AnnotOp(
            annots = (
                'surface_enzyme_go',
                'surface_enzyme_surfaceome',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'surface_enzyme_go',
        source = af.AnnotOp(
            annots = (
                af.AnnotOp(
                    annots = (
                        'cell_surface',
                        af.AnnotDef(
                            name = 'enzyme',
                            source = 'GO_Intercell',
                            args = {
                                'mainclass': 'enzyme',
                            },
                        ),
                        'cell_surface',
                    ),
                    op = set.intersection,
                ),
                'receptor',
            ),
            op = set.difference,
        ),
    ),
    af.AnnotDef(
        name = 'surface_enzyme_surfaceome',
        source = 'Surfaceome',
        args = {
            'mainclass': 'Enzymes',
        },
    ),
    af.AnnotDef(
        name = 'enpp_surface_enzyme_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': (
                'Ectonucleotide pyrophosphatase/phosphodiesterase family'
            ),
        },
    ),  # maybe not all bound to the surface but most of them
    af.AnnotDef(
        name = 'hyaluronidase_surface_enzyme_omnipath',
        source = {'Q9UHN6', 'Q12891', 'P38567', 'Q2M3T9'},
    ),

    # surface ligand
    af.AnnotDef(
        name = 'surface_ligand',
        source = af.AnnotOp(
            annots = (
                'surface_ligand_go',
                'surface_ligand_cellphonedb',
            ),
            op = set.union
        ),
    ),
    af.AnnotDef(
        name = 'surface_ligand_go',
        source = af.AnnotOp(
            annots = (
                'cell_surface',
                'ligand_go',
            ),
            op = set.intersection,
        ),
    ),
    af.AnnotDef(
        name = 'surface_ligand_cellphonedb',
        source = 'CellPhoneDB',
        args = {
            'method': lambda a: (
                not a.receptor and (
                    a.peripheral or
                    a.transmembrane
                )
            ),
        },
    ),
    # surface ligand subclasses from HGNC
    af.AnnotDef(
        name = 'b7_family_surface_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'B7 family',
        },
    ),
    af.AnnotDef(
        name = 'butyrophilin_surface_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Butyrophilins',
        },
    ),
    af.AnnotDef(
        name = 'ephrin_surface_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Ephrins',
        },
    ),
    af.AnnotDef(
        name = 'hedgehog_surface_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Hedgehog signaling molecule family',
        },
    ),  # hedgehog proteins are initially membrane bound and can be
        # solubilized later
    af.AnnotDef(
        name = 'izumo_surface_ligand_hgnc',
        source = {'Q8IYV9', 'Q6UXV1', 'Q5VZ72'},
    ),  # ligands in sperm-egg fusion
    

    # transporter
    af.AnnotDef(
        name = 'transporter',
        source = af.AnnotOp(
            annots = (
                'transporter_surfaceome',
                'transporter_go',
                'transporter_dgidb',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'transporter_surfaceome',
        source = 'Surfaceome',
        args = {
            'mainclass': 'Transporters',
        },
    ),
    af.AnnotDef(
        name = 'transporter_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': {
                'transport',
                'ion channels',
            },
        },
    ),
    af.AnnotDef(
        name = 'transporter_dgidb',
        source = 'DGIdb',
        args = {
            'category': {
                'ABC TRANSPORTER',
                'TRANSPORTER',
                'ION CHANNEL',
            },
        },
    ),

    # transporters from HGNC
    af.AnnotDef(
        name = 'water_transporter_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Aquaporins',
        },
    ),
    af.AnnotDef(
        name = 'bestrophin_transporter_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Bestrophins',
        },
    ),
    af.AnnotDef(
        name = 'abcc_transporter_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'ATP binding cassette subfamily C',
        },
    ),
    af.AnnotDef(
        name = 'abcg_transporter_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'ATP binding cassette subfamily G',
        },
    ),
    af.AnnotDef(
        name = 'hk_atpase_transporter_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'ATPase H+/K+ transporting',
        },
    ),
    af.AnnotDef(
        name = 'nak_atpase_transporter_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'ATPase Na+/K+ transporting subunits',
        },
    ),
    af.AnnotDef(
        name = 'cnnm_metal_transporter_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': (
                'Cyclin and CBS domain divalent metal cation '
                'transport mediators'
            ),
        },
    ),
    af.AnnotDef(
        name = 'acid_sensing_ion_channel_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Acid sensing ion channel subunits',
        },
    ),
    af.AnnotDef(
        name = 'calcium_voltage_gated_ion_channel_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': {
                'Calcium voltage-gated channel alpha1 subunits',
                (
                    'Calcium voltage-gated channel auxiliary '
                    'alpha2delta subunits'
                ),
                ' Calcium voltage-gated channel auxiliary beta subunits',
            },
        },
    ), # these look like all being in cell membrane, but maybe we should
       # filter them?
    af.AnnotDef(
        name = 'catsper_ion_channel_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cation channels sperm associated',
        },
    ),
    af.AnnotDef(
        name = 'chloride_ion_channel_regulator_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Chloride channel accessory',
        },
    ), # in plasma membrane, regulate cholride channels
    af.AnnotDef(
        name = 'chloride_ion_channel_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Chloride channels, ATP-gated CFTR',
        },
    ),
    af.AnnotDef(
        name = 'cyclic_nucleotid_gated_ion_channel_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cyclic nucleotide gated channels',
        },
    ),  # channels gated by various cyclic nucleotides, playing roles in
        # mostly in visual and olfactory signaling
    af.AnnotDef(
        name = 'hydrogen_voltage_gated_ion_channel_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Hydrogen voltage gated channels',
        },
    ),

    # extracellular enzyme
    af.AnnotDef(
        name = 'extracellular_enzyme',
        source = af.AnnotOp(
            annots = (
                'extracellular_enzyme_go',
                'extracellular_enzyme_matrisome',
            ),
            op = set.union
        ),
    ),
    af.AnnotDef(
        name = 'extracellular_enzyme_go',
        source = af.AnnotOp(
            annots = (
                # extracellular by any evidence
                # and enzyme according to GO
                af.AnnotOp(
                    annots = (
                        'extracellular',
                        af.AnnotDef(
                            name = 'enzyme',
                            source = 'GO_Intercell',
                            args = {
                                'mainclass': 'enzyme',
                            },
                        ),
                    ),
                    op = set.intersection,
                ),
                # but not transmembrane or receptor or ligand
                af.AnnotOp(
                    annots = (
                        'transmembrane',
                        'receptor',
                        'ligand',
                    ),
                    op = set.union,
                ),
            ),
            op = set.difference,
        ),
    ),
    af.AnnotDef(
        name = 'extracellular_enzyme_matrisome',
        source = 'Matrisome',
        args = {
            'subclass': 'ECM Regulators',
        },
    ),
    # subclasses from HGNC
    af.AnnotDef(
        name = 'adamts_extracellular_peptidase_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': (
                'ADAM metallopeptidases with thrombospondin type 1 motif'
            ),
        },
    ),
    af.AnnotDef(
        name = 'adamts_like_extracellular_peptidase_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'ADAMTS like',
        },
    ),
    af.AnnotDef(
        name = 'heparanase_extracellular_peptidase_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Heparanases',
        },
    ),  # act on heparin and heparane-sulphate
    af.AnnotDef(
        name = 'defensin_extracellular_enyzme_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': {
                'Defensins, alpha',
                'Defensins, beta',
            },
        },
    ),  # permeabilizing microorganism membranes or
        # binding to microorganism surfaces
    af.AnnotDef(
        name = 'galactosidase_extracellular_enyzme_omnipath',
        source = {'Q6UWU2', 'Q8IW92'},
    ),  # secreted galactosidases
    af.AnnotDef(
        name = 'immune_serin_protease_extracellular_peptidase_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': (
                'Granule associated serine proteases of immune defence'
            ),
        },
    ),  # secreted by granulocytes as part of the immune response
    af.AnnotDef(
        name = 'hyaluronidase_extracellular_enzyme_omnipath',
        source = {'Q12794', 'Q8WUJ3', 'O43820'},
    ),
    af.AnnotDef(
        name = (
            'inter_alpha_trypsin_inhibitor_'
            'extracellular_enyzme_regulator_hgnc'
        ),
        source = 'HGNC',
        args = {
            'mainclass': 'Inter-alpha-trypsin inhibitor heavy chains',
        },
    ),  # protease inhibitors in plasma

    # extracellular peptidase
    af.AnnotDef(
        name = 'extracellular_peptidase_go',
        source = af.AnnotOp(
            annots = (
                'extracellular',
                af.AnnotDef(
                    name = 'peptidase',
                    source = 'GO_Intercell',
                    args = {
                        'mainclass': 'peptidase',
                    },
                ),
            ),
            op = set.intersection,
        ),
    ),
    af.AnnotDef(
        name = 'cela_extracellular_peptidase_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Chymotrypsin like elastases',
        },
    ),  # involved in ECM dynamics and remodeling
    af.AnnotDef(
        name = 'kallikrein_extracellular_peptidase_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Kallikreins',
        },
    ),  # extracellular serine proteases, involved in ECM dynamics

    # growth factor binder or regulator
    af.AnnotDef(
        name = 'growth_factor_binder',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'growth factor binding',
        },
    ),
    af.AnnotDef(
        name = 'growth_factor_regulator',
        source = af.AnnotOp(
            annots = (
                af.AnnotDef(
                    name = 'secreted_matrisome',
                    source = 'Matrisome',
                    args = {
                        'mainclass': 'Matrisome-associated',
                        'subclass': 'Secreted Factors',
                    },
                ),
                af.AnnotOp(
                    annots = (
                        'growth_factor_binder',
                        'extracellular_enzyme',
                    ),
                    op = set.union,
                ),
            ),
            op = set.intersection,
        ),
    ),
    af.AnnotDef(
        name = 'igf_binding_growth_factor_regulator_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Insulin like growth factor binding proteins',
        },
    ),

    # secreted
    af.AnnotDef(
        name = 'secreted',
        source = af.AnnotOp(
            annots = (
                'secreted_locate',
                'secreted_matrisome',
                'secreted_cellphonedb',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'secreted_locate',
        source = 'LOCATE',
        args = {
            'cls': 'secretome',
        },
    ),
    af.AnnotDef(
        name = 'secreted_matrisome',
        source = 'Matrisome',
        args = {
            'mainclass': 'Matrisome-associated',
            'subclass': 'Secreted Factors',
        },
    ),
    af.AnnotDef(
        name = 'secreted_cellphonedb',
        source = 'CellPhoneDB',
        args = {
            'secreted': bool,
        },
    ),
    # specific subclasses from HGNC
    af.AnnotDef(
        name = 'bpi_secreted_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'BPI fold containing',
        },
    ),

    # junctions
    # gap junction
    af.AnnotDef(
        name = 'gap_junction',
        source = af.AnnotOp(
            annots = (
                'gap_junction_go',
                'gap_junction_ramilowski',
                'gap_junction_uniprot',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'gap_junction_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'gap junction',
        },
    ),
    af.AnnotDef(
        name = 'gap_junction_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'gap junction',
        },
    ),
    af.AnnotDef(
        name = 'gap_junction_uniprot',
        source = 'UniProt_location',
        args = {
            'location': 'Gap junction',
        },
    ),
    # tight junction
    af.AnnotDef(
        name = 'tight_junction',
        source = af.AnnotOp(
            annots = (
                'tight_junction_go',
                'tight_junction_ramilowski',
                'tight_junction_uniprot',
            ),
            op = set.union,
        ),
    ),
    af.AnnotDef(
        name = 'tight_junction_go',
        source = 'GO_Intercell',
        args = {
            'mainclass': 'tight junction',
        },
    ),
    af.AnnotDef(
        name = 'tight_junction_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'tight junction',
        },
    ),
    af.AnnotDef(
        name = 'tight_junction_uniprot',
        source = 'UniProt_location',
        args = {
            'location': 'Tight junction',
        },
    ),
    # adherend junction
    af.AnnotDef(
        name = 'adherens_junction_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'adherens junction',
        },
    ),
    # specific subclasses from HGNC
    af.AnnotDef(
        name = 'tight_junction_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Claudins',
        },
    ),
    af.AnnotDef(
        name = 'desmosomal_cadherin_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Desmosomal cadherins',
        },
    ),
    af.AnnotDef(
        name = 'gap_junction_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Gap junction proteins',
        },
    ),

    # plasma membrane regions
    af.AnnotDef(
        name = 'basolateral_cell_membrane_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'basolateral cell membrane',
        },
    ),
    af.AnnotDef(
        name = 'basal_cell_membrane_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'basal cell membrane',
        },
    ),
    af.AnnotDef(
        name = 'basal_cell_membrane_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'basal cell membrane',
        },
    ),
    af.AnnotDef(
        name = 'apical_cell_membrane_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'apical cell membrane',
        },
    ),
    af.AnnotDef(
        name = 'lateral_cell_membrane_ramilowski',
        source = 'Ramilowski_location',
        args = {
            'location': 'lateral cell membrane',
        },
    ),
    # miscellanous from HGNC
    af.AnnotDef(
        name = 'cd_molecule_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'CD molecules',
        }, # membrane proteins, secreted, receptors, enzymes,
           # adhesion proteins
    ),
    af.AnnotDef(
        name = 'c2set_domain_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'C2-set domain containing',
        },
    ),  # these are all plasma membrane proteins, ligands,
        # some receptors and adhesion proteins
    af.AnnotDef(
        name = 'c3_pzp_a2m_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': (
                'C3 and PZP like, alpha-2-macroglobulin domain containing'
            ),
        },  # secreted or peripheral on the outer side of plasma membrane
            # enzymes, protease inhibitors, receptors, co-receptors
    ),

    # to be decided
    af.AnnotDef(
        name = 'bage_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'BAGE family',
        },
    ),
    af.AnnotDef(
        name = 'cap_ctype_lectin_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'CAP and C-type lectin domain containing',
        },
    ), # these are secreted and affect immune signaling
    af.AnnotDef(
        name = 'cmtm_receptor_regulator_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'CKLF like MARVEL transmembrane domain containing',
        },
    ), # transmembrane in plasme membrane; regulate receptor availability
    af.AnnotDef(
        name = 'cacng_ion_channel_regulator_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': ' Calcium channel auxiliary gamma subunits',
        },
    ),  # transmembrane in plasma membrane; regulate calcium channels and
        # glutamate receptors
    af.AnnotDef(
        name = 'calcium_homeostasis_ion_channel_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Calcium homeostasis modulators',
        },
    ), # taste bud ion and ATP channels
    af.AnnotDef(
        name = 'cas_scaffold_intracell_matrix_adhesion_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cas scaffold proteins',
        },
    ), # intracellular part of cell-matrix (focal) adhesion signaling
    af.AnnotDef(
        name = 'cavin_caveolae_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Cavins',
        },
    ), # caveolae formation, intercellular
    af.AnnotDef(
        name = 'clathrin_coated_pit_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Clathrin subunits',
        },
    ), # clathrin coated pit formation, intracellular
    af.AnnotDef(
        name = 'collagen_galactosyltransferase_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Collagen beta(1-O)galactosyltransferases',
        },
    ), # collagen synthesis (in ER)
    af.AnnotDef(
        name = 'complement_system_activator_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Complement system activation components',
        },
    ), # secreted receptors, enzymes and signal transmission proteins
    af.AnnotDef(
        name = 'complement_receptor_and_regulator_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Complement system regulators and receptors',
        },
    ),  # secreted regulators or membrane bound receptors or inhibitors
        # in the complement system downstream signaling
    af.AnnotDef(
        name = 'fibrinogen_c_domain_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Fibrinogen C domain containing',
        },
    ),  # all are secreted, some of them are ligands, enzymes, other kind of
        # regulators for receptors or adhesion, or ECM proteins
    af.AnnotDef(
        name = 'fibronectin_type_iii_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Fibronectin type III domain containing',
        },
    ),  # a mixture of plasma membrane transmembrane receptors or adhesion
        # proteins, and also ECM proteins;
        # a few of them are not extracellular at all
        # probably are annotated in other, more specific categories,
        # especially the `Ig-like cell adhesion molecule family`
    af.AnnotDef(
        name = 'immunoglobulin_like_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Immunoglobulin like domain containing',
        },
    ),  # a mixture of plasma membrane transmembrane receptors or adhesion
        # proteins, and also ECM proteins;
        # a few of them are not extracellular at all
        # probably are annotated in other, more specific categories,
        # especially the `Ig-like cell adhesion molecule family`
    af.AnnotDef(
        name = 'gla_domain_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Gla domain containing',
        },
    ),  # all secreted, various regulators of blood coagulation, ECM,
        # some enzymes or ligands or regulators of other ligands
    af.AnnotDef(
        name = 'hla_surface_ligand_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Histocompatibility complex',
        },
    ),  # histocompatibility antigen complex members for presenting
        # antigens on the cell surface

    # intracellular protein classes in close relation to intercellular
    # communication
    af.AnnotDef(
        name = 'crumbs_complex_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Crumbs complex',
        },
    ),  # scaffolds and regulators for plasma membrane proteins
    af.AnnotDef(
        name = 'engulfment_motility_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Engulfment and cell motility proteins',
        },
    ),  # some intracellular proteins involved in endocytosis
    af.AnnotDef(
        name = 'fbar_actin_dynamics_endocytosis_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'F-BAR domain containing',
        },
    ),  # intracellular proteins, most of them regulate the
        # actin dynamics in endocytosis
    af.AnnotDef(
        name = 'ferm_domain_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'FERM domain containing',
        },
    ),  # intracellular proteins, most of these regulate adhesion and
        # membrane-cytoskeleton interactions; maybe not all related closely
        # to intercellular communication processes
    af.AnnotDef(
        name = 'ferlin_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Ferlin family',
        },
    ),  # intracellular proteins involved in plasma membrane repair
        # and synaptic vesicle fusion
    af.AnnotDef(
        name = 'fermitin_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Fermitins',
        },
    ),  # intracellular proteins, peripheral membrane proteins on the
        # cytoplasmic side of the plasma membrane;
        # involved in cell-cell adhesion
    af.AnnotDef(
        name = 'flotillin_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Flotillins',
        },
    ),  # intracellular proteins with a role in endocytosis
    af.AnnotDef(
        name = 'arc_intracell_omnipath',
        source = {'Q7LC44'},
    ),  # intercellular RNA transfer
    af.AnnotDef(
        name = 'interferon_regulator_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Interferon regulatory factors',
        },
    ),  # intracellular proteins mostly transcriptionally 
        # regulating interferons
    af.AnnotDef(
        name = 'junctophilin_intracell_hgnc',
        source = 'HGNC',
        args = {
            'mainclass': 'Junctophilins',
        },
    ),  # intracellularily connect the plasma membrane and ER to
        # ensure quick response to membrane potential change
    af.AnnotDef(
        name = 'lims1_adhesion_intracell_omnipath',
        source = {'P48059'},
    ),

)

class_types = {
    'above_main': {
        'cell_surface',
        'extracellular',
        'secreted',
        'transmembrane',
        'intracellular',
    },
    'main': {
        'adhesion',
        'ecm',
        'ligand',
        'receptor',
        'surface_enzyme',
        'surface_ligand',
        'transporter',
        'extracellular_enzyme',
    },
    'small_main': {
        'gap_junction',
        'growth_factor_binder',
        'growth_factor_regulator',
        'tight_junction',
    },
    'misc': {
        'extracellular_peptidase',
        'interleukin_receptor_hgnc',
        'interleukin_hgnc',
        'chemokine_ligand_hgnc',
        'endogenous_ligand_hgnc',
    },
}


class_labels = {
    'ecm': 'Extracellular matrix',
    'interleukin_hgnc': 'Interleukins (HGNC)',
    'chemokine_ligand_hgnc': 'Chemokine ligands (HGNC)',
    'endogenous_ligand_hgnc': 'Endogenous ligands (HGNC)',
    'interleukin_receptor_hgnc': 'Interleukin receptors (HGNC)',
}


resource_labels = {
    'cellphonedb': 'CellPhoneDB',
    'topdb': 'TopDB',
    'locate': 'LOCATE',
    'go': 'Gene Ontology',
    'matrixdb': 'MatrixDB',
    'opm': 'OPM',
    'zhong2015': 'Zhong 2015',
    'kirouac': 'Kirouac 2010',
    'hgnc': 'HGNC',
    'hpmr': 'HPMR',
    'cspa': 'CSPA',
    'comppi': 'ComPPI',
    'ramilowski': 'Ramilowski 2015',
    'baccin': 'Baccin 2019',
    'guide2pharma': 'Guide to Pharm',
    'dgidb': 'DGIdb',
    'hpa': 'HPA',
    'lrdb': 'LRdb',
}


def get_label(key, exceptions):

    return (
        exceptions[key]
            if key in exceptions else
        key.replace('_', ' ').capitalize()
    )


def get_class_label(class_key):

    return get_label(class_key, class_labels)


def get_resource_label(resource_key):

    return get_label(resource_key, resource_labels)
