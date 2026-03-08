from security.auth_manager import AuthManager

def test_authentication():

    auth = AuthManager()

    auth.register_node("node1", "cert123")

    assert auth.authenticate("node1", "cert123")
