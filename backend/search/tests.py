from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from search.views import RoutesListAPIView
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
# from search.serializers import MyModelSerializer

from .models import Descriptor, NodeSimilarity, MousePheno, Hgene, Hprotein, Intact, Pathway, Reactome, Signor, Gwas



class CountViewTests(APITestCase):
    def test_get_entity_count(self):
        """
        Test that the count of a specific entity type is returned correctly.
        """
        type_string = "hgene"

        # Mock the get_entity_count function to return a known value
        with patch('search.views.CountView') as mock:
            
            mock.return_value = '8847039'

            url = reverse('search:count_entity', kwargs={'type_string': type_string})
            response = self.client.get(url)

            # Check that the response has the expected status code and data
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content.decode('utf-8'), '8847039')


            
            # data = json.loads(content)
            # assert data == '8847039'

            # Check that the get_entity_count function was called with the expected argument
            # mock.assert_called_once_with(type_string)

    # def test_get_entity_count_error(self):
    #     """
    #     Test that an error response is returned when get_entity_count raises an exception.
    #     """
    #     type_string = "invalid_entity_type"

    #     # Mock the get_entity_count function to raise an exception
    #     with patch('search.views.CountView') as mock_get_entity_count:
    #         mock_get_entity_count.side_effect = Exception('Invalid entity type: invalid_entity_type')

    #         url = reverse('search:count_entity', kwargs={'type_string': type_string})
    #         response = self.client.get(url)

    #         # Check that the response has the expected status code and error message
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #         self.assertEqual(response.content.decode('utf-8'), {'error': 'Invalid entity type: invalid_entity_type'})

    #         # Check that the get_entity_count function was called with the expected argument
    #         mock_get_entity_count.assert_called_once_with(type_string)



class DescriptorListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('search:descriptors')
        self.descriptor1 = Descriptor.objects.create(name='Pathway')
        self.descriptor2 = Descriptor.objects.create(name='Reactome')

    def test_get_descriptors_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Check that the first descriptor in the response has the expected name
        self.assertEqual(response.data[0]['name'], self.descriptor1.name)

        # Check that the second descriptor in the response has the expected name
        self.assertEqual(response.data[1]['name'], self.descriptor2.name)

class DescriptorModelTests(TestCase):
    def setUp(self):
        Descriptor.objects.create(name="Reactome")

    def test_descriptor_name(self):
        test_descriptor = Descriptor.objects.get(name="Reactome")
        self.assertEqual(test_descriptor.name, "Reactome")


class NodeSimilarityModelTests(TestCase):
    def setUp(self):
        NodeSimilarity.objects.create(target1="DRD3", target2="NLGN3", similarity=0.22)

    def test_similarity_score(self):
        test_similarity = NodeSimilarity.objects.get(target1="DRD3", target2="NLGN3")
        self.assertEqual(test_similarity.similarity, 0.22)


class MousePhenoModelTests(TestCase):
    def setUp(self):
        MousePheno.objects.create(target1="DRD3", target2="ENSG00000224931", similarity=0.75)

    def test_mousepheno_similarity(self):
        test_similarity = MousePheno.objects.get(target1="DRD3", target2="ENSG00000224931")
        self.assertEqual(test_similarity.similarity, 0.75)


class HgeneModelTests(TestCase):
    def setUp(self):
        Hgene.objects.create(target1="IGLV1-44", target2="IGHV5-51", similarity=0.9125)

    def test_hgene_similarity(self):
        test_similarity = Hgene.objects.get(target1="IGLV1-44", target2="IGHV5-51")
        self.assertEqual(test_similarity.similarity, 0.9125)


class HproteinModelTests(TestCase):
    def setUp(self):
        Hprotein.objects.create(target1="Target1", target2="Target2", similarity=0.5)

    def test_hprotein_similarity(self):
        test_similarity = Hprotein.objects.get(target1="Target1", target2="Target2")
        self.assertEqual(test_similarity.similarity, 0.5)


class IntactModelTests(TestCase):
    def setUp(self):
        Intact.objects.create(target1="TATDN3", target2="PKD1L1-AS1", similarity=0.5)

    def test_intact_similarity(self):
        test_similarity = Intact.objects.get(target1="TATDN3", target2="PKD1L1-AS1")
        self.assertEqual(test_similarity.similarity, 0.5)


class PathwayModelTests(TestCase):
    def setUp(self):
        Pathway.objects.create(target1="ANTXR2", target2="MAP2K1", similarity=0.125)

    def test_pathway_similarity(self):
        test_similarity = Pathway.objects.get(target1="ANTXR2", target2="MAP2K1")
        self.assertEqual(test_similarity.similarity, 0.125)


class ReactomeModelTests(TestCase):
    def setUp(self):
        Reactome.objects.create(target1="CD55", target2="C4BPB", similarity=0.4)

    def test_reactome_similarity(self):
        test_similarity = Reactome.objects.get(target1="CD55", target2="C4BPB")
        self.assertEqual(test_similarity.similarity, 0.4)


class SignorModelTests(TestCase):
    def setUp(self):
        Signor.objects.create(target1="IL1RAP", target2="ITGA3", similarity=0.25)

    def test_signor_similarity(self):
        test_similarity = Signor.objects.get(target1="IL1RAP", target2="ITGA3")
        self.assertEqual(test_similarity.similarity, 0.25)


class GwasModelTests(TestCase):
    def setUp(self):
        test_similarity = Gwas.objects.create(target1="Target1", target2="Target2", similarity=0.5)
        self.assertEqual(test_similarity.similarity, 0.5)
