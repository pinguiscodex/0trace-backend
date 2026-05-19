import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_openapi_schema_generation_succeeds(tmp_path):
    output = tmp_path / "openapi.yaml"

    call_command("spectacular", file=str(output), validate=True, verbosity=0)

    contents = output.read_text()
    assert "0trace API" in contents
    assert "/api/v1/auth/signup/" in contents
    assert "/api/v1/browser/resolve/" in contents

