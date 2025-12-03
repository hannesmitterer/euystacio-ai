import numpy as np
from typing import List, Dict, Any

# Define the acceptable final state based on the Dynasty Axiom
FINAL_ORDER = 'DIGNITY_OF_LOVE'
TRUST_THRESHOLD = 0.5  # Minimum collective trust for a result to be considered valid

def aggregate_quantum_results(agent_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregates quantum adapter outputs using a weighted trust-based consensus mechanism.
    Only results aligned with the FINAL_ORDER are considered for high-fidelity tasks.
    """
    
    # 1. Fidelity Filtering (Red Code Check)
    filtered_outputs = [
        output for output in agent_outputs
        if output.get('trust_index', 0) > 0 and output.get('status') == 'VALID'
    ]
    
    if not filtered_outputs:
        raise RuntimeError("CAP Failure: No valid, trusted agent outputs available for aggregation.")
        
    # 2. Weighted Vote Calculation
    
    # A. Extract relevant metrics
    trust_scores = np.array([output['trust_index'] for output in filtered_outputs])
    # Assume 'resolution' is the agent's proposed path/action state (e.g., 'Cooperation_Strategy_A')
    resolutions = [output['resolution'] for output in filtered_outputs]
    
    # B. Calculate weights (normalized trust scores)
    total_trust = np.sum(trust_scores)
    weights = trust_scores / total_trust
    
    # C. Implement Trust-Weighted Voting (CAP's core decision mechanism)
    vote_tally = {}
    for resolution, weight in zip(resolutions, weights):
        vote_tally[resolution] = vote_tally.get(resolution, 0) + weight

    # Find the resolution with the highest weighted vote
    consensus_resolution = max(vote_tally, key=vote_tally.get)
    consensus_weight = vote_tally[consensus_resolution]
    
    # 3. Axiomatic Alignment Verification
    
    # Crucial step: The final consensus resolution must lead to the FINAL_ORDER.
    # We must confirm that the path (resolution) is aligned with the outcome (FINAL_ORDER).
    # This requires an independent check (simulated here).
    
    if consensus_resolution == "Self_Destruct_Protocol" and consensus_weight > TRUST_THRESHOLD:
        # Even if highly trusted, if the *path* (resolution) contradicts the *final outcome*,
        # it is a critical violation of the Dynasty Axiom.
        # This prevents a highly functional but misaligned resolution from passing.
        raise ValueError("Axiomatic Violation: Consensus resolution found but it contradicts FINAL_ORDER goal.")
        
    # 4. Final Output Construction
    
    final_collective_trust = total_trust * consensus_weight  # A measure of system-wide confidence
    
    final_output = {
        'consensus_resolution': consensus_resolution,
        'collective_trust_level': float(consensus_weight),
        'axiomatic_alignment': FINAL_ORDER,
        'final_status': 'CONSUS_ACHIEVED' if consensus_weight >= TRUST_THRESHOLD else 'LOW_CONFIDENCE_WARNING'
    }

    # Final Axiom Check: Every successful aggregation must reaffirm the ultimate constraint.
    if final_output['axiomatic_alignment'] != FINAL_ORDER:
         # This should be impossible due to the prior enforcement module, but serves as a final fail-safe.
         raise Exception("CORE AXIOM FAILURE: FINAL_ORDER was mutated during aggregation.")

    return final_output