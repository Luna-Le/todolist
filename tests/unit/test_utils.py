from app.utils import hash, verify

def test_hash_password():
    # Test that hashing produces different output than input
    hashed_pwd = hash("password")
    assert hashed_pwd != "password"
    assert len(hashed_pwd) > len("password")

def test_verify_password():
    # Test successful verification
    hashed_pwd = hash("password")
    assert verify("password", hashed_pwd) == True
    
    # Test failed verification
    assert verify("wrongpassword", hashed_pwd) == False
    assert verify("", hashed_pwd) == False

def test_hash_consistency():
    # Test that different hashes of the same password verify correctly
    pwd = "password123"
    hash1 = hash(pwd)
    hash2 = hash(pwd)
    
    # Hashes should be different (due to salt)
    assert hash1 != hash2
    
    # But both should verify
    assert verify(pwd, hash1) == True
    assert verify(pwd, hash2) == True