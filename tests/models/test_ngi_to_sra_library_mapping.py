from snpseq_metadata.models.ngi_to_sra_library_mapping import (
    ApplicationSampleTypeMapping,
    UnspecifiedLibrary,
    ReadyMadeLibrary,
    TargetCaptureExome,
    RNASeqKitMRNA,
)


class TestApplicationSampleTypeMapping:
    @staticmethod
    def _create_object_helper(
        expected_cls,
        application="this-is-an-application",
        sample_type="this-is-a-sample-type",
        sample_prep_kit="this-is-a-sample-prep-kit",
    ):
        assert (
            ApplicationSampleTypeMapping.create_object(
                application=application,
                sample_type=sample_type,
                sample_prep_kit=sample_prep_kit,
            )
            == expected_cls
        )

    def test_create_object_unspecified(self):
        """
        trying to match something unknown should return an unspecified library
        """
        self._create_object_helper(UnspecifiedLibrary)

    def test_create_object_rml(self):
        self._create_object_helper(
            ReadyMadeLibrary,
            application="ready-made library",
            sample_type="ready-made library",
        )
        # test with an application that should be partially matched
        self._create_object_helper(
            ReadyMadeLibrary,
            application="rml-this-is-an-application",
            sample_type="ready-made library",
        )

    def test_create_object_single_class(self):
        self._create_object_helper(
            TargetCaptureExome,
            application="target re-seq",
            sample_type="gdna",
            sample_prep_kit="twist human core exome",
        )

    def test_create_object_final_class(self):
        self._create_object_helper(
            RNASeqKitMRNA,
            application="rna-seq",
            sample_type="total rna",
            sample_prep_kit="truseq stranded mrna sample preparation kit ht",
        )
