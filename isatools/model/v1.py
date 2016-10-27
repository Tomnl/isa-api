# coding: utf-8
"""ISA Model 1.0 implementation in Python.

This module implements the ISA Abstract Model 1.0 as Python classes, as
specified in the `ISA Model and Serialization Specifications 1.0`_, and
additional classes to support compatibility between ISA-Tab and ISA-JSON.

Todo:
    * Check consistency with published ISA Model
    * Finish docstringing rest of the module
    * Add constraints on attributes throughout, and test

.. _ISA Model and Serialization Specifications 1.0: http://isa-specs.readthedocs.io/

"""
from __future__ import absolute_import

import networkx as nx
import six

from .utils import accepts

def _build_assay_graph(process_sequence=list()):
    G = nx.DiGraph()
    for process in process_sequence:
        if process.next_process is not None or process.outputs:  # first check if there's some valid outputs to connect
            if process.outputs:
                for output in (n for n in process.outputs if not isinstance(n, DataFile)):
                    G.add_edge(process, output)
            else:  # otherwise just connect the process to the next one
                G.add_edge(process, process.next_process)
        #if process.prev_process is not None or process.inputs > 0:
        if process.inputs:
            for input_ in process.inputs:
                G.add_edge(input_, process)
        elif process.prev_process is not None:
            G.add_edge(process.prev_process, process)
    return G


class Comment(object):
    """A comment allows arbitrary annotation of all ISA classes

    Comments are implemented in ISA-Tab and ISA-JSON formats.

    Attributes:
        name (str): The name of the comment (as mapped to Comment[SomeName] in ISA-Tab) to give context to the comment field
        value (str, int, float, NoneType): A value for the corresponding comment, as a string or number
    """
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    @property
    def name(self):
        return self.__name

    @name.setter
    @accepts(six.text_type, None, allow_empty=False)
    def name(self, name):
        self.__name = name

    @property
    def value(self):
        if not self.__value:
            return None
        else:
            return self.__value

    @value.setter
    @accepts(six.text_type, int, float, None)
    def value(self, value):
        self.__value = value


class Commentable(object):
    """ An ISA Object is an abstract class to enable containment of Comments

    Attributes:
        comments (list, NoneType): Comments associated with the implementing ISA class (all ISA classes)
    """
    def __init__(self, comments=None):
        self.comments = comments

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    @accepts(list, None)
    def comments(self, comments):
        self.__comments = comments


class Investigation(Commentable):
    """An investigation maintains metadata about the project context and links to one or more studies. There can only
    be 1 Investigation in an ISA package. Investigations has the following properties:

    Attributes:
        identifier: A locally unique identifier or an accession number provided by a repository.
        title: A concise name given to the investigation
        description: A textual description of the investigation
        submission_date: The date on which the investigation was reported to the repository.
        public_release_date: The date on which the investigation should be released publicly
        ontology_source_references: This annotation section is identical to that in the MAGE-TAB format.
        publications: Publications associated with an Investigation.
        contacts: People/contacts associated with an Investigation.
        studies: Study is the central unit, containing information on the subject under study, its characteristics and
        any treatments applied.
    """

    def __init__(self, id_='', filename='', identifier="", title="", description="", submission_date='',
                 public_release_date='', ontology_source_references=None, publications=None,
                 contacts=None, studies=None, comments=None):
        super(Investigation, self).__init__(comments)
        self.id = id_
        self.filename = filename
        self.identifier = identifier
        self.title = title
        self.description = description
        self.submission_date = submission_date
        self.public_release_date = public_release_date
        if ontology_source_references is None:
            self.ontology_source_references = list()
        else:
            self.ontology_source_references = ontology_source_references
        if publications is None:
            self.publications = list()
        else:
            self.publications = publications
        if contacts is None:
            self.contacts = list()
        else:
            self.contacts = contacts
        if studies is None:
            self.studies = list()
        else:
            self.studies = studies
        if comments is None:
            self.comments = list()


class OntologySource(Commentable):
    """An OntologySource describes the resource from which the value of an OntologyAnnotation is derived from.

    Attributes:
        name (str): The name of the source of a term; i.e. the source controlled vocabulary or ontology.
        file (str, NoneType): A file name or a URI of an official resource.
        version (str, NoneType): The version number of the Term Source to support terms tracking.
        description (str, NoneType): A free text description of the resource.
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, name, file=None, version=None, description=None, comments=None):
        super(OntologySource, self).__init__(comments)
        self.name = name
        self.file = file
        self.version = version
        self.description = description

    @property
    def name(self):
        return self.__name

    @name.setter
    @accepts(six.text_type, None, allow_empty=False)
    def name(self, name):
        self.__name = name

    @property
    def file(self):
        if not self.__file:
            return None
        else:
            return self.__file

    @file.setter
    @accepts(six.text_type, None)
    def file(self, file):
        self.__file = file

    @property
    def version(self):
        if not self.__version:
            return None
        else:
            return self.__version

    @version.setter
    @accepts(six.text_type, None)
    def version(self, version):
        self.__version = version

    @property
    def description(self):
        if not self.__description:
            return None
        else:
            return self.__description

    @description.setter
    @accepts(six.text_type, None)
    def description(self, description):
        self.__description = description


class OntologyAnnotation(Commentable):
    """An ontology annotation

    Attributes:
        term (str, NoneType): A term taken from an ontology or controlled vocabulary.
        term_source (OntologySource): Reference to the resource from which the term is derived.
        term_accession (str, NoneType): A URI or resource-specific identifier for the term.
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, term=None, term_source=None, term_accession=None, comments=None, id_=''):
        super(OntologyAnnotation, self).__init__(comments)

        self.term = term
        self.term_source = term_source
        self.term_accession = term_accession
        self.id = id_

    @property
    def term(self):
        if not self.__term:
            return None
        else:
            return self.__term

    @term.setter
    @accepts(six.text_type, None)
    def term(self, term):
        self.__term = term

    @property
    def term_source(self):
        return self.__term_source

    @term_source.setter
    @accepts(OntologySource, None)
    def term_source(self, term_source):
        self.__term_source = term_source

    @property
    def term_accession(self):
        if not self.__term:
            return None
        else:
            return self.__term_accession

    @term_accession.setter
    @accepts(six.text_type, None)
    def term_accession(self, term_accession):
        self.__term_accession = term_accession


class Publication(Commentable):
    """A publication associated with an investigation or study.

    Attributes:
        pubmed_id (str, NoneType): The PubMed IDs of the described publication(s) associated with this investigation.
        doi (str, NoneType): A Digital Object Identifier (DOI) for that publication (where available).
        author_list (str, NoneType): The list of authors associated with that publication.
        title (str, NoneType): The title of publication associated with the investigation.
        status(str, OntologyAnnotation, NoneType): A term describing the status of that publication (i.e. submitted,
            in preparation, published).
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, pubmed_id=None, doi=None, author_list=None, title=None, status=None, comments=None):
        super(Publication, self).__init__(comments)
        self.pubmed_id = pubmed_id
        self.doi = doi
        self.author_list = author_list
        self.title = title
        self.status = status

        @property
        def pubmed_id(self):
            if not self.__pubmed_id:
                return None
            else:
                return self.__pubmed_id

        @pubmed_id.setter
        @accepts(six.text_type, None)
        def pubmed_id(self, pubmed_id):
            self.__pubmed_id = pubmed_id

        @property
        def doi(self):
            if not self.__doi:
                return None
            else:
                return self.__doi

        @doi.setter
        @accepts(six.text_type, None)
        def doi(self, doi):
            self.__doi = doi

        @property
        def author_list(self):
            if not self.__author_list:
                return None
            else:
                return self.__author_list

        @author_list.setter
        @accepts(six.text_type, None)
        def doi(self, author_list):
            self.__author_list = author_list

        @property
        def status(self):
            if not self.__status:
                return None
            else:
                return self.__status

        @status.setter
        @accepts(OntologyAnnotation, six.text_type, None)
        def status(self, status):
            self.__status = status


class Person(Commentable):
    """A person/contact that can be attributed to an Investigation or Study.

    Attributes:
        last_name (str, NoneType): The last name of a person associated with the investigation.
        first_name (str, NoneType): The first name of a person associated with the investigation.
        mid_initials (str, NoneType): The middle initials of a person associated with the investigation.
        email (str, NoneType): The email address of a person associated with the investigation.
        phone (str, NoneType): The telephone number of a person associated with the investigation.
        fax (str, NoneType): The fax number of a person associated with the investigation.
        address (str, NoneType): The address of a person associated with the investigation.
        affiliation (str, NoneType): The organization affiliation for a person associated with the investigation.
        roles (list, NoneType): OntologyAnnotations to classify the role(s) performed by this person in the context of
        the investigation, which means that the roles reported here need not correspond to roles held withing their
        affiliated organization.
        comments (list, NoneType): Comments associated with instances of this class.
    """

    def __init__(self, first_name=None, last_name=None, mid_initials=None, email=None, phone=None, fax=None,
                 address=None, affiliation=None, roles=None, comments=None, id_=''):
        super(Person, self).__init__(comments)
        self.id = id_
        self.last_name = last_name
        self.first_name = first_name
        self.mid_initials = mid_initials
        self.email = email
        self.phone = phone
        self.fax = fax
        self.address = address
        self.affiliation = affiliation
        self.roles = roles


class Study(Commentable, object):
    """Study is the central unit, containing information on the subject under study, its characteristics
    and any treatments applied.

    Attributes:
        identifier: A unique identifier: either a temporary identifier supplied by users or one generated by a
        repository or other database.
        title: A concise phrase used to encapsulate the purpose and goal of the study.
        description: A textual description of the study, with components such as objective or goals.
        submission_date: The date on which the study is submitted to an archive.
        public_release_date: The date on which the study should be released publicly.
        file_name: A field to specify the name of the Study file corresponding the definition of that Study.
        design_descriptors: Classifications of the study based on the overall experimental design.
        publications: Publications associated with a Study.
        contacts: People/contacts associated with a Study.
        factors: A factor corresponds to an independent variable manipulated by the experimentalist with the intention
        to affect biological systems in a way that can be measured by an assay.
        protocols: Protocols used within the ISA artifact.
        assays: An Assay represents a portion of the experimental design.
        data: Data files associated with the study
    """

    def __init__(self, id_='', filename="", identifier="",  title="", description="", submission_date='',
                 public_release_date='', contacts=None, design_descriptors=None, publications=None,
                 factors=None, protocols=None, assays=None, sources=None, samples=None,
                 process_sequence=None, other_material=None, characteristic_categories=None, comments=None, units=None):
        super(Study, self).__init__(comments)
        self.id = id_
        self.filename = filename
        self.identifier = identifier
        self.title = title
        self.description = description
        self.submission_date = submission_date
        self.public_release_date = public_release_date

        if publications is None:
            self.publications = list()
        else:
            self.publications = publications

        if contacts is None:
            self.contacts = list()
        else:
            self.contacts = contacts

        if design_descriptors is None:
            self.design_descriptors = list()
        else:
            self.design_descriptors = design_descriptors

        if protocols is None:
            self.protocols = list()
        else:
            self.protocols = protocols

        if units is None:
            self.units = list()
        else:
            self.units = units

        self.materials = {
            'sources': list(),
            'samples': list(),
            'other_material': list()
        }
        if sources is not None:
            self.materials['sources'].append(sources)
        if samples is not None:
            self.materials['samples'].append(samples)
        if other_material is not None:
            self.materials['other_material'].append(other_material)

        if process_sequence is None:
            self.process_sequence = list()
        else:
            self.process_sequence = process_sequence

        if assays is None:
            self.assays = list()
        else:
            self.assays = assays

        if factors is None:
            self.factors = list()
        else:
            self.factors = factors

        if characteristic_categories is None:
            self.characteristic_categories = list()
        else:
            self.characteristic_categories = characteristic_categories
        self.graph = None

    #     self.__graph = None

    # @property
    # def graph(self):
    #     if len(self.process_sequence) > 0:
    #         self.__graph = _build_assay_graph(self.process_sequence)
    #     else:
    #         self.__graph = None
    #     return self.__graph
    #
    # @graph.setter
    # def graph(self, graph):
    #     raise AttributeError("Study.graph is not settable")


class StudyFactor(Commentable):
    """A Study Factor corresponds to an independent variable manipulated by the experimentalist with the intention to
    affect biological systems in a way that can be measured by an assay.

    Attributes:
        name: Study factor name
        factor_type: An ontology source reference of the study factor type
    """

    def __init__(self, id_='', name="", factor_type=None, comments=None):
        super(StudyFactor, self).__init__(comments)
        self.id = id_
        self.name = name
        if factor_type is None:
            self.factor_type = OntologyAnnotation()
        else:
            self.factor_type = factor_type


class Assay(Commentable):
    """A Study Assay declares and describes each of the Assay files associated with the current Study.

    Attributes:
        measurement_type: A term to qualify the endpoint, or what is being measured (e.g. gene expression profiling or
        protein identification). The term can be free text or from, for example, a controlled vocabulary or an ontology.
        technology_type: Term to identify the technology used to perform the measurement, e.g. DNA microarray, mass
        spectrometry. The term can be free text or from, for example, a controlled vocabulary or an ontology.
        technology_platform: Manufacturer and platform name, e.g. Bruker AVANCE
        file_name: A field to specify the name of the Assay file corresponding the definition of that assay.
    """
    def __init__(self, measurement_type=None, technology_type=None, technology_platform="", filename="",
                 process_sequence=None, data_files=None, samples=None, other_material=None,
                 characteristic_categories=None, comments=None):
        super(Assay, self).__init__(comments)
        if measurement_type is None:
            self.measurement_type = OntologyAnnotation()
        else:
            self.measurement_type = measurement_type

        if technology_type is None:
            self.technology_type = OntologyAnnotation()
        else:
            self.technology_type = technology_type

        self.technology_platform = technology_platform
        self.filename = filename

        if process_sequence is None:
            self.process_sequence = list()
        else:
            self.process_sequence = process_sequence

        if data_files is None:
            self.data_files = list()
        else:
            self.data_files = data_files

        self.materials = {
            'samples': list(),
            'other_material': list()
        }

        if not (samples is None):
            self.materials['samples'].append(samples)

        if not (other_material is None):
            self.materials['other_material'].append(other_material)

        if characteristic_categories is None:
            self.characteristic_categories = list()
        else:
            self.characteristic_categories = characteristic_categories
        self.graph = None
        # self.__graph = None

    # @property
    # def graph(self):
    #     if len(self.process_sequence) > 0:
    #         self.__graph = _build_assay_graph(self.process_sequence)
    #     else:
    #         self.__graph = None
    #     return self.__graph
    #
    # @graph.setter
    # def graph(self, graph):
    #     raise AttributeError("Assay.graph is not settable")


class Protocol(Commentable):
    """A Protocol.

    Attributes:
        name:
        protocol_type:
        description:
        version:
        parameters:
        components:
    """
    def __init__(self, id_='', name="", protocol_type=None, uri="", description="", version="", parameters=None,
                 components=None, comments=None):
        super(Protocol, self).__init__(comments)
        self.id = id_
        self.name = name
        if protocol_type is None:
            self.protocol_type = OntologyAnnotation()
        else:
            self.protocol_type = protocol_type
        self.description = description
        self.uri = uri
        self.version = version
        if parameters is None:
            self.parameters = list()
        else:
            self.parameters = parameters
        if components is None:
            self.components = list()
        else:
            self.components = components


class ProtocolParameter(Commentable):
    """A Protocol Parameter.

    Attributes:
        name:
        unit:
    """
    def __init__(self, id_='', parameter_name=None, unit=None, comments=None):
        super(ProtocolParameter, self).__init__(comments)
        self.id = id_
        if parameter_name is None:
            self.parameter_name = OntologyAnnotation()
        else:
            self.parameter_name = parameter_name
        # if unit is None:
        #     self.unit = OntologyAnnotation()
        # else:
        #     self.unit = unit


class ProtocolComponent(Commentable):
    def __init__(self, id_='', name='', component_type=None, comments=None):
        super(ProtocolComponent, self).__init__(comments)
        self.id = id_
        self.name = name
        if component_type is None:
            self.component_type = OntologyAnnotation()
        else:
            self.component_type = component_type


class Source(Commentable):
    """A Source.

    Attributes:
        name:
        characteristics:
    """
    def __init__(self, id_='', name="", characteristics=None, comments=None):
        super(Source, self).__init__(comments)
        self.id = id_
        self.name = name
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics


class Characteristic(Commentable):
    def __init__(self, category=None, value=None, unit=None, comments=None):
        super(Characteristic, self).__init__(comments)
        if category is None:
            self.category = OntologyAnnotation()
        else:
            self.category = category
        if value is None:
            self.value = OntologyAnnotation()
        else:
            self.value = value
        self.unit = unit


class Sample(Commentable):
    """A Sample.

    Attributes:
        name:
        characteristics:
        factors:
    """
    def __init__(self, id_='', name="", factor_values=None, characteristics=None, derives_from=None, comments=None):
        super(Sample, self).__init__(comments)
        self.id = id_
        self.name = name
        if factor_values is None:
            self.factor_values = list()
        else:
            self.factor_values = factor_values
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics
        self.derives_from = derives_from


class Material(Commentable):
    """A Material.

    Attributes:
        name:
        characteristics:
    """
    def __init__(self, id_='', name="", type_='', characteristics=None, derives_from=None, comments=None):
        super(Material, self).__init__(comments)
        self.id = id_
        self.name = name
        self.type = type_
        if characteristics is None:
            self.characteristics = list()
        else:
            self.characteristics = characteristics
        self.derives_from = derives_from


class Extract(Material):
    def __init__(self, id_='', name="", type_='', characteristics=None, derives_from=None, comments=None):
        super(Extract, self).__init__(id_, name, type_, characteristics, derives_from, comments)
        self.type = 'Extract Name'


class LabeledExtract(Extract):
    def __init__(self, id_='', name="", type_='', characteristics=None, derives_from=None, comments=None, label=None):
        super(LabeledExtract, self).__init__(id_, name, type_, characteristics, derives_from, comments)
        self.label = label


class FactorValue(Commentable):
    def __init__(self, factor_name=None, value=None, unit=None, comments=None):
        super(FactorValue, self).__init__(comments)
        self.factor_name = factor_name
        self.value = value
        self.unit = unit


class Process(Commentable):
    """A Process.

    Attributes:
        name:
        executes_protocol:
        parameters:
        inputs:
        outputs:
    """
    def __init__(self, id_='', name="", executes_protocol=None, date_=None, performer=None,
                 parameter_values=None, inputs=None, outputs=None, comments=None):
        super(Process, self).__init__(comments)
        self.id = id_
        self.name = name
        if executes_protocol is None:
            self.executes_protocol = Protocol()
        else:
            self.executes_protocol = executes_protocol
        self.date = date_
        self.performer = performer
        if parameter_values is None:
            self.parameter_values = list()
        else:
            self.parameter_values = parameter_values
        if inputs is None:
            self.inputs = list()
        else:
            self.inputs = inputs
        if outputs is None:
            self.outputs = list()
        else:
            self.outputs = outputs
        self.additional_properties = dict()
        self.prev_process = None
        self.next_process = None


class DataFile(Commentable):
    def __init__(self, id_='', filename='', label='', comments=None):
        super(DataFile, self).__init__(comments)
        self.id = id_
        self.filename = filename
        self.label = label


def batch_create_materials(material=None, n=1):
    """Creates a batch of material objects (Source, Sample or Material) from a prototype material object

    :param material: existing material object to use as a prototype
    :param n: Number of material objects to create in the batch
    :returns: List of material objects

    :Example:

        # Create 10 sample materials derived from one source material

        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material', derives_from=source)
        batch = batch_create_materials(prototype_sample, n=10)

        [Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, ]

    """
    material_list = list()
    if isinstance(material, (Source, Sample, Material)):
        from copy import deepcopy
        for x in six.moves.range(n):
            new_obj = deepcopy(material)
            new_obj.name = '-'.join([material.name, str(x)])
            material_list.append(new_obj)
    return material_list


def batch_create_assays(*args, **kwargs):
    """Creates a batch of assay process sequences (Material->Process->Material) from a prototype sequence
    (currently works only as flat end-to-end processes of Material->Process->Material->...)

    :param *args: An argument list representing the process sequence prototype
    :param n: Number of process sequences to create in the batch
    :returns: List of process sequences replicating the prototype sequence

    :Example:

        # Create 3 assays of (Sample -> Process -> Material -> Process -> LabeledExtract)

        sample = Sample(name='sample')
        data_acquisition = Process(name='data acquisition')
        material = Material(name='material')
        labeling = Process(name='labeling')
        extract = LabeledExtract(name='lextract')
        batch = batch_create_assays(sample, data_acquisition, material, labeling, extract, n=3)

        [Process<> Process<>, Process<> Process<>, Process<>, Process<>]

        # Create 3 assays of ([Sample, Sample] -> Process -> [Material, Material])

        sample1 = Sample(name='sample')
        sample2 = Sample(name='sample')
        process = Process(name='data acquisition')
        material1 = Material(name='material')
        material2 = Material(name='material')
        batch = batch_create_assays([sample1, sample2], process, [material1, material2], n=3)

    """
    n = kwargs['n'] if 'n' in kwargs else 1
    process_sequence = list()
    materialA = None
    process = None
    materialB = None
    from copy import deepcopy
    for x in six.moves.range(n):
        for arg in args:
            if isinstance(arg, list) and arg:
                if isinstance(arg[0], (Sample, Material)):
                    if materialA is None:
                        materialA = deepcopy(arg)
                        y = 0
                        for material in materialA:
                            material.name = '-'.join([material.name, str(x), str(y)])
                            y += 1
                    else:
                        materialB = deepcopy(arg)
                        y = 0
                        for material in materialB:
                            material.name = '-'.join([material.name, str(x), str(y)])
                            y += 1
                elif isinstance(arg[0], Process):
                    process = deepcopy(arg)
                    y = 0
                    for p in process:
                        p.name = '-'.join([p.name, str(x), str(y)])
                        y += 1
            if isinstance(arg, (Sample, Material)):
                if materialA is None:
                    materialA = deepcopy(arg)
                    materialA.name = '-'.join([materialA.name, str(x)])
                else:
                    materialB = deepcopy(arg)
                    materialB.name = '-'.join([materialB.name, str(x)])
            elif isinstance(arg, Process):
                process = deepcopy(arg)
                process.name = '-'.join([process.name, str(x)])
            if materialA is not None and materialB is not None and process is not None:
                if isinstance(process, list):
                    for p in process:
                        if isinstance(materialA, list):
                            p.inputs = materialA
                        else:
                            p.inputs.append(materialA)
                        if isinstance(materialB, list):
                            p.outputs = materialB
                            for material in materialB:
                                material.derives_from = materialA
                        else:
                            p.outputs.append(materialB)
                            materialB.derives_from = materialA
                else:
                    if isinstance(materialA, list):
                        process.inputs = materialA
                    else:
                        process.inputs.append(materialA)
                    if isinstance(materialB, list):
                        process.outputs = materialB
                        for material in materialB:
                            material.derives_from = materialA
                    else:
                        process.outputs.append(materialB)
                        materialB.derives_from = materialA
                    process_sequence.append(process)
                materialA = materialB
                process = None
                materialB = None
    return process_sequence


def batch_set_attr(l=list(), attr=None, val=None):
    for i in l:
        setattr(i, attr, val)


class ParameterValue(object):
    """A Parameter Value
    """
    def __init__(self, category=None, value=None, unit=None):
        super(ParameterValue, self).__init__()
        # if category is None:
        #     raise TypeError("You must specify a category")
        self.category = category
        self.value = value
        self.unit = unit
