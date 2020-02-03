#!/usr/bin/env python3

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

"""

This module use cffi to access the c functions in the amcl_mpc library.

"""
import cffi
import platform
import os

ffi = cffi.FFI()
ffi.cdef("""

typedef long unsigned int BIG_512_60[9];
typedef long unsigned int BIG_1024_58[18];

typedef struct {
unsigned int ira[21];  /* random number...   */
int rndptr;   /* ...array & pointer */
unsigned int borrow;
int pool_ptr;
char pool[32];    /* random pool */
} csprng;

typedef struct
{
  int len;
  int max;
  char *val;
} octet;

/*!
 * \brief Paillier Public Key
 */
typedef struct
{
    BIG_512_60 n[8]; /**< Paillier Modulus - \f$ n = pq \f$ */
    BIG_512_60 g[8]; /**< Public Base - \f$ g = n+1 \f$ */

    BIG_512_60 n2[8]; /**< Precomputed \f$ n^2 \f$ */
} PAILLIER_public_key;

/*!
 * \brief Paillier Private Key
 */
typedef struct
{
    BIG_1024_58 p[1]; /**< Secret Prime */
    BIG_1024_58 q[1]; /**< Secret Prime */

    BIG_1024_58 lp[1]; /**< Private Key modulo \f$ p \f$ (Euler totient of \f$ p \f$) */
    BIG_1024_58 lq[1]; /**< Private Key modulo \f$ q \f$ (Euler totient of \f$ q \f$) */

    BIG_1024_58 invp[2]; /**< Precomputed \f$ p^{-1} \pmod{2^m} \f$ */
    BIG_1024_58 invq[2]; /**< Precomputed \f$ q^{-1} \pmod{2^m} \f$ */

    BIG_1024_58 p2[2]; /**< Precomputed \f$ p^2 \f$ */
    BIG_1024_58 q2[2]; /**< Precomputed \f$ q^2 \f$ */

    BIG_1024_58 mp[1]; /**< Precomputed \f$ L(g^{lp} \pmod{p^2})^{-1} \f$ */
    BIG_1024_58 mq[1]; /**< Precomputed \f$ L(g^{lq} \pmod{q^2})^{-1} \f$ */
} PAILLIER_private_key;

extern void RAND_seed(csprng *R,int n,char *b);
extern void RAND_clean(csprng *R);
extern void OCT_clear(octet *O);

extern void PAILLIER_KEY_PAIR(csprng *RNG, octet *P, octet* Q, PAILLIER_public_key *PUB, PAILLIER_private_key *PRIV);
extern void PAILLIER_PRIVATE_KEY_KILL(PAILLIER_private_key *PRIV);

extern int  ECP_SECP256K1_KEY_PAIR_GENERATE(csprng *R,octet *s,octet *W);
extern int  ECP_SECP256K1_PUBLIC_KEY_VALIDATE(octet *W);

extern int MPC_ECDSA_VERIFY(octet *HM,octet *PK, octet *R,octet *S);
extern void MPC_MTA_CLIENT1(csprng *RNG, PAILLIER_public_key* PUB, octet* A, octet* CA, octet* R);
extern void MPC_MTA_CLIENT2(PAILLIER_private_key *PRIV, octet* CB, octet *ALPHA);
extern void MPC_MTA_SERVER(csprng *RNG, PAILLIER_public_key *PUB, octet *B, octet *CA, octet *Z, octet *R, octet *CB, octet *BETA);
extern void MPC_SUM_MTA(octet *A, octet *B, octet *ALPHA, octet *BETA, octet *SUM);
extern void MPC_INVKGAMMA(octet *KGAMMA1, octet *KGAMMA2, octet *INVKGAMMA);
extern extern int MPC_R(octet *INVKGAMMA, octet *GAMMAPT1, octet *GAMMAPT2, octet *R);
extern void MPC_HASH(int sha, octet *M, octet *HM);
extern int MPC_S(octet *HM, octet *R, octet *K, octet *SIGMA, octet *S);
extern void MPC_SUM_S(octet *S1, octet *S2, octet *S);
extern int MPC_SUM_PK(octet *PK1, octet *PK2, octet *PK);
extern void MPC_DUMP_PAILLIER_PK(PAILLIER_public_key *PUB, octet *N, octet *G, octet *N2);
extern void MPC_LOAD_PAILLIER_PK(PAILLIER_public_key *PUB, octet *N, octet *G, octet *N2);
extern void MPC_DUMP_PAILLIER_SK(PAILLIER_private_key *PRIV, octet *P, octet *Q, octet *LP, octet *LQ, octet *INVP, octet *INVQ, octet *P2, octet *Q2, octet *MP, octet *MQ);
extern void MPC_LOAD_PAILLIER_SK(PAILLIER_private_key *PRIV, octet *P, octet *Q, octet *LP, octet *LQ, octet *INVP, octet *INVQ, octet *P2, octet *Q2, octet *MP, octet *MQ);

""")

if (platform.system() == 'Windows'):
    libamcl_mpc = ffi.dlopen("libamcl_mpc.dll")
    libamcl_paillier = ffi.dlopen("libamcl_paillier.dll")
    libamcl_curve_secp256k1 = ffi.dlopen("libamcl_curve_SECP256K1.dll")    
    libamcl_core = ffi.dlopen("libamcl_core.dll")
elif (platform.system() == 'Darwin'):
    libamcl_mpc = ffi.dlopen("libamcl_mpc.dylib")
    libamcl_paillier = ffi.dlopen("libamcl_paillier.dylib")    
    libamcl_curve_secp256k1 = ffi.dlopen("libamcl_curve_SECP256K1.dylib")
    libamcl_core = ffi.dlopen("libamcl_core.dylib")
else:
    libamcl_mpc = ffi.dlopen("libamcl_mpc.so")
    libamcl_paillier = ffi.dlopen("libamcl_paillier.so")
    libamcl_curve_secp256k1 = ffi.dlopen("libamcl_curve_SECP256K1.so")    
    libamcl_core = ffi.dlopen("libamcl_core.so")


# Constants
FS_2048 = 256
HFS_2048 = 128
FS_4096 = 512
EGS_SECP256K1 = 32
PTS_SECP256K1 = 2*EGS_SECP256K1 + 1
SHA256 = 32
curve_order = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

def to_str(octet_value):
    """Converts an octet type into a string

    Add all the values in an octet into an array.

    Args::

        octet_value. An octet pointer type

    Returns::

        String

    Raises:
        Exception
    """
    i = 0
    val = []
    while i < octet_value.len:
        val.append(octet_value.val[i])
        i = i + 1
    out = b''
    for x in val:
        out = out + x
    return out


def make_octet(length, value=None):
    """Generates an octet pointer

    Generates an empty octet or one filled with the input value

    Args::

        length: Length of empty octet
        value:  Data to assign to octet

    Returns::

        oct_ptr: octet pointer
        val: data associated with octet to prevent garbage collection

    Raises:

    """
    oct_ptr = ffi.new("octet*")
    if value:
        val = ffi.new("char [%s]" % len(value), value)
        oct_ptr.val = val
        oct_ptr.max = len(value)
        oct_ptr.len = len(value)
    else:
        val = ffi.new("char []", length)
        oct_ptr.val = val
        oct_ptr.max = length
        oct_ptr.len = length
    return oct_ptr, val


def create_csprng(seed):
    """Make a Cryptographically secure pseudo-random number generator instance

    Make a Cryptographically secure pseudo-random number generator instance

    Args::

        seed:   random seed value

    Returns::

        rng: Pointer to cryptographically secure pseudo-random number generator instance

    Raises:

    """
    seed_val = ffi.new("char [%s]" % len(seed), seed)
    seed_len = len(seed)

    # random number generator
    rng = ffi.new('csprng*')
    libamcl_core.RAND_seed(rng, seed_len, seed_val)

    return rng


def kill_csprng(rng):
    """Kill a random number generator

    Deletes all internal state

    Args::

        rng: Pointer to cryptographically secure pseudo-random number generator instance

    Returns::

    Raises:

    """
    libamcl_core.RAND_clean(rng)

    return 0

def paillier_key_pair(rng, p=None, q=None):
    """Generate Paillier key pair

    Generate Paillier key pair

    Args::

        rng: Pointer to cryptographically secure pseudo-random number generator instance
        p: p prime number. Externally generated
        q: q prime number. Externally generated

    Returns::

        paillier_pk: Paillier public key
        paillier_sk: Paillier secret key

    Raises:

    """
    if p:
        p1, p1_val = make_octet(None, p)
        q1, q1_val = make_octet(None, q)        
        rng = ffi.NULL
    else:
        p1 = ffi.NULL 
        q1 = ffi.NULL               

    paillier_pk = ffi.new('PAILLIER_public_key*')
    paillier_sk = ffi.new('PAILLIER_private_key*')    
    
    libamcl_paillier.PAILLIER_KEY_PAIR(rng, p1, q1, paillier_pk, paillier_sk)

    return paillier_pk, paillier_sk

def paillier_private_key_kill(paillier_sk):
    """Kill a Paillier secret key

    Deletes all internal state

    Args::

        paillier_sk: Pointer to Paillier secret key

    Returns::



    Raises:

    """
    libamcl_paillier.PAILLIER_PRIVATE_KEY_KILL(PAILLIER_private_key *PRIV);

    return 0

def ecp_secp256k1_key_pair_generate(rng, ecdsa_sk=None):
    """Generate ECDSA key pair

    Generate ECDSA key pair

    Args::

        rng: Pointer to cryptographically secure pseudo-random number generator instance
        ecdsa_sk: secret key input

    Returns::

        ecdsa_sk: ECDSA secret key
        ecdsa_pk: ECDSA public key
        rc: Zero for success or else an error code

    Raises:

    """
    if ecdsa_sk:
        ecdsa_sk1, ecdsa_sk1_val = make_octet(None, ecdsa_sk)
        rng = ffi.NULL
    else:
        ecdsa_sk1, ecdsa_sk1_val = make_octet(EGS_SECP256K1)        

    ecdsa_pk1, ecdsa_pk1_val = make_octet(PTS_SECP256K1)                

    rc = libamcl_curve_secp256k1.ECP_SECP256K1_KEY_PAIR_GENERATE(rng, ecdsa_sk1, ecdsa_pk1)

    ecdsa_sk2 = to_str(ecdsa_sk1)
    ecdsa_pk2 = to_str(ecdsa_pk1)    
    
    return rc, ecdsa_pk2, ecdsa_sk2

def ecp_secp256k1_public_key_validate(ecdsa_pk):    
    """Validate an ECDSA public key

    Validate an ECDSA public key

    Args::

        ecdsa_pk: ECDSA public key

    Returns::

        rc: Zero for success or else an error code

    Raises:

    """
    ecdsa_pk1, ecdsa_pk1_val = make_octet(None, ecdsa_pk)

    rc = libamcl_curve_secp256k1.ECP_SECP256K1_PUBLIC_KEY_VALIDATE(ecdsa_pk1)
    
    return rc

def mpc_mta_client1(rng, paillier_pk, a, r=None):
    """Client MTA first pass

    Client MTA first pass

    Args::

        rng: Pointer to cryptographically secure pseudo-random number generator instance
        paillier_pk: Pointer to Paillier public keys
        a: Multiplicative share of secret
        r: R value for testing. 

    Returns::

        ca: Ciphertext of additive share of secret
        r: R value for testing.

    Raises:

    """
    if r:
        r1, r1_val = make_octet(None, r)
        rng = ffi.NULL
    else:
        r1 = ffi.NULL

    a1, a1_val = make_octet(None, a)
    ca1, ca1_val = make_octet(FS_4096)        
    
    libamcl_mpc.MPC_MTA_CLIENT1(rng, paillier_pk, a1, ca1, r1)

    ca2 = to_str(ca1)
    
    return ca2

def mpc_mta_client2(paillier_sk, cb):
    """Client MtA second pass

    Client MTA first pass

    Args::

        paillier_sk: Pointer to Paillier secret key
        cb: Ciphertext to decrypt

    Returns::

        alpha: Additive share of secret

    Raises:

    """
    cb1, cb1_val = make_octet(None, cb)
    alpha1, alpha1_val = make_octet(EGS_SECP256K1)        
    
    libamcl_mpc.MPC_MTA_CLIENT2(paillier_sk, cb1, alpha1)

    alpha2 = to_str(alpha1)
    
    return alpha2

def mpc_mta_server(rng, paillier_pk, b, ca, z=None, r=None):
    """Server MtA

    Server MtA

    Args::

        rng: Pointer to cryptographically secure pseudo-random number generator instance
        paillier_pk: Pointer to Paillier public key
        b: Multiplicative share of secret
        ca: Ciphertext of client's additive share of secret
        z: Negative of beta value used for testing
        r: r value for testing.

    Returns::

        cb: Ciphertext 
        beta: Additive share of secret 

    Raises:

    """
    if r:
        r1, r1_val = make_octet(None, r)
        z1, z1_val = make_octet(None, z)        
        rng = ffi.NULL
    else:
        r1 = ffi.NULL        
        z1 = ffi.NULL        

    b1, b1_val = make_octet(None, b)
    ca1, ca1_val = make_octet(None, ca)            
    beta1, beta1_val = make_octet(EGS_SECP256K1)        
    cb1, cb1_val = make_octet(FS_4096)        
    
    libamcl_mpc.MPC_MTA_SERVER(rng, paillier_pk, b1, ca1, z1, r1, cb1, beta1)

    beta2 = to_str(beta1)
    cb2 = to_str(cb1)    
    
    return cb2, beta2

def mpc_sum_mta(a, b, alpha, beta):
    """Sum of secret shares

    Sum of secret shares

    Args::

        a1: A1 Value
        b1: B1 Value
        alpha: Additive share of A1.B2
        beta: Additive share of A2.B1

    Returns::

        sum: The sum of all values

    Raises:

    """
    a1, a1_val = make_octet(None, a)
    b1, b1_val = make_octet(None, b)
    alpha1, alpha1_val = make_octet(None, alpha)
    beta1, beta1_val = make_octet(None, beta)
    
    sum1, sum1_val = make_octet(EGS_SECP256K1)
    
    libamcl_mpc.MPC_SUM_MTA(a1, b1, alpha1, beta1, sum1);

    sum2 = to_str(sum1)
    
    return sum2

def mpc_invkgamma(kgamma1, kgamma2):
    """Calculate the inverse of the sum of kgamma values

    Calculate the inverse of the sum of kgamma values

    Args::

        kgamma1: Actor 1 additive share
        kgamma2: Actor 2 additive share

    Returns::

        invkgamma: Inverse of the sum of the additive shares

    Raises:

    """
    kgamma11, kgamma11_val = make_octet(None, kgamma1)
    kgamma21, kgamma21_val = make_octet(None, kgamma2)    
    
    invkgamma1, invkgamma1_val = make_octet(EGS_SECP256K1)
    
    libamcl_mpc.MPC_INVKGAMMA(kgamma11, kgamma21, invkgamma1)

    invkgamma2 = to_str(invkgamma1)
    
    return invkgamma2

def mpc_r(invkgamma, gammapt1, gammapt2):
    """R component

    Generate the ECDSA signature R component

    Args::

        invkgamma: Inverse of k times gamma
        gammapt1: Actor 1 gamma point
        gammapt2: Actor 2 gamma point

    Returns::

        r: R component of the signature
        rc: Zero for success or else an error code

    Raises:

    """
    invkgamma1, invkgamma1_val = make_octet(None, invkgamma)
    gammapt11, gammapt11_val = make_octet(None, gammapt1)
    gammapt21, gammapt21_val = make_octet(None, gammapt2)    
    
    r1, r1_val = make_octet(EGS_SECP256K1)
    
    rc = libamcl_mpc.MPC_R(invkgamma1, gammapt11, gammapt21, r1)

    r2 = to_str(r1)
    
    return rc, r2

def mpc_hash(message):
    """Hash the message value

    Hash the message value using sha256

    Args::

        message: Message to be hashed

    Returns::

        hm: hash of message 

    Raises:

    """
    message1, message1_val = make_octet(None, message)
    hm1, hm1_val = make_octet(SHA256)
    
    libamcl_mpc.MPC_HASH(SHA256, message1, hm1)

    hm2 = to_str(hm1)
    
    return hm2

def mpc_s(hm, r, k, sigma):
    """S component

    Generate the ECDSA signature S component

    Args::

        hm: Hash of the message to be signed
        r: r component of signature
        k: nonce value
        sigma: Additive share of k.w

    Returns::

        s: s signature component output
        rc: Zero for success or else an error code

    Raises:

    """
    hm1, hm1_val = make_octet(None, hm)
    r1, r1_val = make_octet(None, r)
    k1, k1_val = make_octet(None, k)
    sigma1, sigma1_val = make_octet(None, sigma)    

    s1, s1_val = make_octet(EGS_SECP256K1)
    
    rc = libamcl_mpc.MPC_S(hm1, r1, k1, sigma1, s1)

    s2 = to_str(s1)
    
    return rc, s2

def mpc_ecdsa_verify(hm, pk, r, s):
    """ECDSA Verify signature

    Verify the ECDSA signature (R,S) on a message

    Args::

        hm: Hash of the message to be verify
        pk: ecdsa public key
        r: r component of signature
        s: s component of signature

    Returns::

        rc: Zero for success or else an error code

    Raises:

    """
    hm1, hm1_val = make_octet(None, hm)
    pk1, pk1_val = make_octet(None, pk)
    r1, r1_val = make_octet(None, r)
    s1, s1_val = make_octet(None, s)        
    
    rc = libamcl_mpc.MPC_ECDSA_VERIFY(hm1, pk1, r1, s1)

    return rc

def mpc_sum_s(s1, s2):
    """Sum of ECDSA s components

    Calculate the sum of the s components of the ECDSA signature

    Args::

        s1: Actor 1 ECDSA s component
        s2: Actor 2 ECDSA s component

    Returns::

        s: The sum of all ECDSA s shares

    Raises:

    """
    s11, s11_val = make_octet(None, s1)
    s21, s21_val = make_octet(None, s2)    
    
    s1, s1_val = make_octet(EGS_SECP256K1)
    
    libamcl_mpc.MPC_SUM_S(s11, s21, s1);

    s2 = to_str(s1)
    
    return s2

def mpc_sum_pk(pk1, pk2):
    """Sum of ECDSA public key shares

    Calculate the sum of the ECDSA public key shares

    Args::

        pk1: Actor 1 ECDSA public key share
        pk2: Actor 2 ECDSA public key share

    Returns::

        pk: The sum of all ECDSA pk shares
        rc: Zero for success or else an error code

    Raises:

    """
    pk11, pk11_val = make_octet(None, pk1)
    pk21, pk21_val = make_octet(None, pk2)    
    
    pk1, pk1_val = make_octet(PTS_SECP256K1)

    rc = libamcl_mpc.MPC_SUM_PK(pk11, pk21, pk1);

    pk2 = to_str(pk1)
    
    return rc, pk2

def mpc_dump_paillier_pk(paillier_pk):
    """Write Paillier public key to byte array

    Write Paillier public key to byte array

    Args::

        paillier_pk: Pointer to Paillier public key

    Returns::

        n: Paillier Modulus - n = pq
        g: Public Base - g = n+1
        n2: Precomputed - n^2 

    Raises:

    """
    n1, n1_val = make_octet(FS_4096)
    g1, g1_val = make_octet(FS_4096)
    n21, n21_val = make_octet(FS_4096)    
    
    libamcl_mpc.MPC_DUMP_PAILLIER_PK(paillier_pk, n1, g1, n21)

    n2 = to_str(n1)
    g2 = to_str(g1)
    n22 = to_str(n21)        

    return n2, g2, n22

def mpc_load_paillier_pk(n,g,n2):
    """Read Paillier public key from byte arrays

    Read Paillier public key from byte arrays

    Args::

        n: Paillier Modulus - n = pq
        g: Public Base - g = n+1
        n2: Precomputed - n^2 

    Returns::

        paillier_pk: Pointer to Paillier public key

    Raises:

    """
    paillier_pk = ffi.new('PAILLIER_public_key*')

    n1, n1_val = make_octet(None, n)
    g1, g1_val = make_octet(None, g)
    n21, n21_val = make_octet(None, n2)        


    libamcl_mpc.MPC_LOAD_PAILLIER_PK(paillier_pk, n1, g1, n21)

    return paillier_pk

def mpc_dump_paillier_sk(paillier_sk):
    """Write Paillier public key to byte array

    Write Paillier public key to byte array

    Args::

        paillier_sk: Pointer to Paillier secret key

    Returns::

        p:           Secret prime number 
        q:           Secret prime number 
        lp:          Private Key modulo \f$ p \f$ (Euler totient of \f$ p \f$)
        lq:          Private Key modulo \f$ q \f$ (Euler totient of \f$ q \f$)
        invp:        Precomputed \f$ p^{-1} \pmod{2^m} \f$
        invq:        Precomputed \f$ q^{-1} \pmod{2^m} \f$
        p2:          Precomputed \f$ p^2 \f$
        q2:          Precomputed \f$ q^2 \f$ 
        mp:          Precomputed \f$ L(g^{lp} \pmod{p^2})^{-1} \f$
        mq:          Precomputed \f$ L(g^{lq} \pmod{q^2})^{-1} \f$

    Raises:

    """
    p, p_val = make_octet(HFS_2048)
    q, q_val = make_octet(HFS_2048)    

    lp, lp_val = make_octet(HFS_2048)
    lq, lq_val = make_octet(HFS_2048)    

    invp, invp_val = make_octet(FS_2048)
    invq, invq_val = make_octet(FS_2048)    

    pp2, pp2_val = make_octet(FS_2048)
    qq2, qq2_val = make_octet(FS_2048)    
    
    mp, mp_val = make_octet(HFS_2048)
    mq, mq_val = make_octet(HFS_2048)    
    
    libamcl_mpc.MPC_DUMP_PAILLIER_SK(paillier_sk, p, q, lp, lq, invp, invq, pp2, qq2, mp, mq)

    p2 = to_str(p)
    q2 = to_str(q)

    lp2 = to_str(lp)
    lq2 = to_str(lq)    

    invp2 = to_str(invp)
    invq2 = to_str(invq)    

    p22 = to_str(pp2)
    q22 = to_str(qq2)    

    mp2 = to_str(mp)
    mq2 = to_str(mq)    
    
    return p2, q2, lp2, lq2, invp2, invq2, p22, q22, mp2, mq2

def mpc_load_paillier_sk(p, q, lp, lq, invp, invq, p2, q2, mp, mq):
    """Read Paillier secret key from byte arrays

    Read Paillier secret key from byte arrays

    Args::

        p:           Secret prime number 
        q:           Secret prime number 
        lp:          Private Key modulo \f$ p \f$ (Euler totient of \f$ p \f$)
        lq:          Private Key modulo \f$ q \f$ (Euler totient of \f$ q \f$)
        invp:        Precomputed \f$ p^{-1} \pmod{2^m} \f$
        invq:        Precomputed \f$ q^{-1} \pmod{2^m} \f$
        p2:          Precomputed \f$ p^2 \f$
        q2:          Precomputed \f$ q^2 \f$ 
        mp:          Precomputed \f$ L(g^{lp} \pmod{p^2})^{-1} \f$
        mq:          Precomputed \f$ L(g^{lq} \pmod{q^2})^{-1} \f$

    Returns::

        paillier_sk: Pointer to Paillier secret key

    Raises:

    """
    paillier_sk = ffi.new('PAILLIER_private_key*')

    p1, p1_val = make_octet(None, p)
    q1, q1_val = make_octet(None, q)   

    lp1, lp1_val = make_octet(None, lp)
    lq1, lq1_val = make_octet(None, lq)

    invp1, invp1_val = make_octet(None, invp)
    invq1, invq1_val = make_octet(None, invq)

    p21, p21_val = make_octet(None, p2)
    q21, q21_val = make_octet(None, q2)    
    
    mp1, mp1_val = make_octet(None, mp)
    mq1, mq1_val = make_octet(None, mq)    

    libamcl_mpc.MPC_LOAD_PAILLIER_SK(paillier_sk,  p1, q1, lp1, lq1, invp1, invq1, p21, q21, mp1, mq1)

    return paillier_sk