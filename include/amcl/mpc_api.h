/*
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
*/

/**
 * @file mpc_api.h
 * @brief MPC API declarations
 *
 */

#ifndef MPC_API_H
#define MPC_API_H

#define SEEDLEN 16 //!< Entropy source length in bytes

#include <amcl/amcl.h>

#ifdef __cplusplus
extern "C" {
#endif

/*! \brief Generate an ECDSA public/private key pair
 *
 *  @param   seed             Seed value for cryptographically secure random number generator
 *  @param   sk               Secret key
 *  @param   pk               Public key
 *  @return                   Returns 0 or else error code
 */
int mpc_api_ecdsa_keys(char* seed, char* sk, char* pk);

/*! \brief Generate the paillier key pair
 *
 *  Pick large prime numbers of the same size \f$ p \f$ and \f$ q \f$
 *
 *  <ol>
 *  <li> \f$ n = pq \f$
 *  <li> \f$ g = n + 1 \f$
 *  <li> \f$ l = (p-1)(q-1) \f$
 *  <li> \f$ m = l^{-1} \pmod{n} \f$
 *  </ol>
 *
 *  @param  seed             Seed value for cryptographically secure random number generator
 *  @param  p                Prime number.
 *  @param  q                Prime number.
 *  @param  n                Public key (see above)
 *  @param  g                Public key (see above)
 *  @param  l                Private key (see above)
 *  @param  m                Private key (see above)
 *  @return                  Returns 0 or else error code
 */
int mpc_api_paillier_keys(char* seed, char* p, char* q, char* n, char* g, char* l, char* m);

/*! \brief Generate an ECDSA public/private key pair
 *

 *  @param   sk               Secret key
 *  @param   pk               Public key
 *  @return                   Returns 0 or else error code
 */

/*! \brief Client MTA first pass
 *
 *  Encrypt multplicative share, \f$ a \f$, of secret \f$ s = a.b \f$
 *
 *  @param  seed             Seed value for cryptographically secure random number generator
 *  @param  n                Public key
 *  @param  g                Public key
 *  @param  a                Multiplicative share of secret
 *  @param  ca               Ciphertext
 *  @param  r                R value for testing. If RNG is NULL then this value is read.
 *  @return                  Returns 0 or else error code
 */
int mpc_api_mta_client1(char* seed, char* n, char* g, char* a, char* ca, char* r);


/*! \brief Server MtA
 *
 *  Calculate additive share, \f$ \beta \f$, of secret \f$ s = a.b \f$ and
 *  ciphertext allowing client to calculate their additive share.
 *
 *  <ol>
 *  <li> Choose a random non-zero value \f$ z \in  F_q \f$ where \f$q\f$ is the curve order
 *  <li> \f$ \beta = -z\text{ }\mathrm{mod}\text{ }q \f$
 *  <li> \f$ cb = ca \otimes{} b \oplus{} z = E_A(ab + z) \f$
 *  </ol>
 *
 *  @param  seed             Seed value for cryptographically secure random number generator
 *  @param   N                Public key
 *  @param   G                Public key
 *  @param   B                Multiplicative share of secret
 *  @param   CA               Ciphertext of client's additive share of secret
 *  @param   Z                Plaintext z value (see above)
 *  @param   R                R value for testing. If RNG is NULL then this value is read.
 *  @param   CB               Ciphertext
 *  @param   BETA             Additive share of secret (see above)
 *  @return                   Returns 0 or else error code
 */
int mpc_api_mta_server(char* seed, char* n, char* g, char* b, char* ca, char* z, char* r, char* cb, char* beta);

/*! \brief Client MtA second pass
 *
 *  Calculate additive share, \f$ \alpha \f$, of secret \f$ s = a.b \f$
 *
 *  <ol>
 *  <li> Choose a random non-zero value \f$ z \in  F_q \f$ where \f$q\f$ is the curve order
 *  <li> \f$ \alpha = D_A(cb) = D_A(E_A(ab + z)) = ab + z \text{ }\mathrm{mod}\text{ }q \f$
 *  </ol>
 *
 *  @param   n                Public key
 *  @param   l                Private key
 *  @param   m                Private key
 *  @param   cb               Ciphertext
 *  @param   alpha            Additive share of secret
 *  @return                   Returns 0 or else error code
 */
int mpc_api_mta_client2(char* n, char* l, char* m, char* cb, char* alpha);

/** \brief Sum of secret shares
 *
 *  Sum of secret shares generated by multiplicative to additive scheme
 *
 *  <ol>
 *  <li> \f$ sum  = a.b + \alpha{}1 + \beta{}1 + \alpha{}2 + \beta{}2 \text{ }\mathrm{mod}\text{ }q \f$
 *  </ol>
 *
 *  @param a                  a1 value
 *  @param b                  b1 value
 *  @param alpha1             Additive share of a1.b2
 *  @param beta1              Additive share of a2.b1
 *  @param alpha2             Additive share of a1.b3
 *  @param beta2              Additive share of a3.b1
 *  @param sum                The sum of all values
 *  @return                   Returns 0 or else error code
 */
int mpc_api_sum_mta(char* a, char* b, char* alpha1, char* beta1, char* alpha2, char* beta2, char* sum);

#ifdef __cplusplus
}
#endif

#endif
