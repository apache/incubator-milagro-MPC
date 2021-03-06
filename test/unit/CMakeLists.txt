# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# Add the binary tree directory to the search path for linking and include files
link_directories (${PROJECT_BINARY_DIR}/src
                  /usr/local/lib)

include_directories (${PROJECT_SOURCE_DIR}/src
                     ${PROJECT_SOURCE_DIR}/include
                     ${PROJECT_SOURCE_DIR}/test
                     /usr/local/include)

function(amcl_test name source dependencies expected_response)
  add_executable(${name} "${source}" $<TARGET_OBJECTS:mpc_test_utils>)

  target_link_libraries(${name} PRIVATE ${dependencies})

  add_test(NAME ${name}
    COMMAND ${TARGET_SYSTEM_EMULATOR} $<TARGET_FILE:${name}> ${ARGN}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/testVectors
  )

  set_tests_properties(${name} PROPERTIES
    PASS_REGULAR_EXPRESSION "${expected_response}"
  )
endfunction()

# MPC tests
amcl_test(test_mta           test_mta.c           amcl_mpc "SUCCESS" "mpc/MTA.txt")
amcl_test(test_r             test_r.c             amcl_mpc "SUCCESS" "mpc/R.txt")
amcl_test(test_s             test_s.c             amcl_mpc "SUCCESS" "mpc/S.txt")
amcl_test(test_phase5_commit test_phase5_commit.c amcl_mpc "SUCCESS" "mpc/phase5_commit.txt")
amcl_test(test_phase5_prove  test_phase5_prove.c  amcl_mpc "SUCCESS" "mpc/phase5_prove.txt")
amcl_test(test_phase5_verify test_phase5_verify.c amcl_mpc "SUCCESS" "mpc/phase5_verify.txt")

# NM Commitment tests
amcl_test(test_nm_commit test_nm_commit.c amcl_mpc "SUCCESS" "commitments/nm_commit.txt")

# ZKP of knowledge of factoring
amcl_test(test_factoring_zk_prove  test_factoring_zk_prove.c  amcl_mpc "SUCCESS" "factoring_zk/prove.txt")
amcl_test(test_factoring_zk_verify test_factoring_zk_verify.c amcl_mpc "SUCCESS" "factoring_zk/verify.txt")

# Classic Schnorr tests
amcl_test(test_schnorr_commit    test_schnorr_commit.c    amcl_mpc "SUCCESS" "schnorr/commit.txt")
amcl_test(test_schnorr_challenge test_schnorr_challenge.c amcl_mpc "SUCCESS" "schnorr/challenge.txt")
amcl_test(test_schnorr_prove     test_schnorr_prove.c     amcl_mpc "SUCCESS" "schnorr/prove.txt")
amcl_test(test_schnorr_verify    test_schnorr_verify.c    amcl_mpc "SUCCESS" "schnorr/verify.txt")

# Double Schnorr tests
amcl_test(test_d_schnorr_commit    test_d_schnorr_commit.c    amcl_mpc "SUCCESS" "schnorr/dcommit.txt")
amcl_test(test_d_schnorr_challenge test_d_schnorr_challenge.c amcl_mpc "SUCCESS" "schnorr/dchallenge.txt")
amcl_test(test_d_schnorr_prove     test_d_schnorr_prove.c     amcl_mpc "SUCCESS" "schnorr/dprove.txt")
amcl_test(test_d_schnorr_verify    test_d_schnorr_verify.c    amcl_mpc "SUCCESS" "schnorr/dverify.txt")

# BC Commitment tests
amcl_test(test_bc_setup     test_bc_setup.c     amcl_mpc "SUCCESS" "commitments/bc_setup.txt")
amcl_test(test_bc_internals test_bc_internals.c amcl_mpc "SUCCESS")

# MTA Range Proof tests
amcl_test(test_mta_rp_commit    test_mta_rp_commit.c    amcl_mpc "SUCCESS" "mta/rp_commit.txt")
amcl_test(test_mta_rp_challenge test_mta_rp_challenge.c amcl_mpc "SUCCESS" "mta/rp_challenge.txt")
amcl_test(test_mta_rp_prove     test_mta_rp_prove.c     amcl_mpc "SUCCESS" "mta/rp_prove.txt")
amcl_test(test_mta_rp_verify    test_mta_rp_verify.c    amcl_mpc "SUCCESS" "mta/rp_verify.txt")
amcl_test(test_mta_rp_octets    test_mta_rp_octets.c    amcl_mpc "SUCCESS" "mta/rp_verify.txt")

# MTA Receiver ZK Proof
amcl_test(test_mta_zk_commit    test_mta_zk_commit.c    amcl_mpc "SUCCESS" "mta/mta_commit.txt")
amcl_test(test_mta_zk_challenge test_mta_zk_challenge.c amcl_mpc "SUCCESS" "mta/mta_challenge.txt")
amcl_test(test_mta_zk_prove     test_mta_zk_prove.c     amcl_mpc "SUCCESS" "mta/mta_prove.txt")
amcl_test(test_mta_zk_verify    test_mta_zk_verify.c    amcl_mpc "SUCCESS" "mta/mta_verify.txt")
amcl_test(test_mta_zk_octets    test_mta_zk_octets.c    amcl_mpc "SUCCESS" "mta/mta_verify.txt")

# MTAWC Receiver ZK Proof
amcl_test(test_mta_zkwc_commit    test_mta_zkwc_commit.c    amcl_mpc "SUCCESS" "mta/mtawc_commit.txt")
amcl_test(test_mta_zkwc_challenge test_mta_zkwc_challenge.c amcl_mpc "SUCCESS" "mta/mtawc_challenge.txt")
amcl_test(test_mta_zkwc_prove     test_mta_zkwc_prove.c     amcl_mpc "SUCCESS" "mta/mtawc_prove.txt")
amcl_test(test_mta_zkwc_verify    test_mta_zkwc_verify.c    amcl_mpc "SUCCESS" "mta/mtawc_verify.txt")
amcl_test(test_mta_zkwc_octets    test_mta_zkwc_octets.c    amcl_mpc "SUCCESS" "mta/mtawc_verify.txt")
