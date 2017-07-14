"""Tests on Assay planning model objects in isatools.create.models"""
import unittest

from isatools.create.models import AssayType

MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING = 'transcription profiling'
TECHNOLOGY_TYPE_DNA_MICROARRAY = 'DNA microarray'
TECHNOLOGY_TYPE_DNA_SEQUENCING = 'nucleic acid sequencing'


class AssayTypeTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.assay_type = AssayType(
            measurement_type=MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
            technology_type=TECHNOLOGY_TYPE_DNA_MICROARRAY
        )

    def test_repr(self):
        self.assertEqual('AssayType(mt={0}, tt={1})'.format(
            MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
            TECHNOLOGY_TYPE_DNA_MICROARRAY
        ), repr(self.assay_type))

    def test_eq(self):
        expected_assay_type = AssayType(
            measurement_type=MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
            technology_type=TECHNOLOGY_TYPE_DNA_MICROARRAY
        )
        self.assertEqual(expected_assay_type, self.assay_type)
        self.assertEqual(hash(expected_assay_type), hash(self.assay_type),)

    def test_ne(self):
        expected_other_assay_type = AssayType(
            measurement_type=MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
            technology_type=TECHNOLOGY_TYPE_DNA_SEQUENCING
        )
        self.assertNotEqual(expected_other_assay_type, self.assay_type)
        self.assertNotEqual(hash(expected_other_assay_type), hash(self.assay_type))