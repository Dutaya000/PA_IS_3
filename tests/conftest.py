import pytest

# Configura pytest para manejar corrutinas asíncronas automáticamente
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
