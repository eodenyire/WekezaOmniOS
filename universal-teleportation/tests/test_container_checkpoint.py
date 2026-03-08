from runtime_adapters.container_checkpoint import checkpoint_container

def test_checkpoint():

    container_id = "example"

    checkpoint = checkpoint_container(container_id)

    assert checkpoint == "uat-checkpoint"
