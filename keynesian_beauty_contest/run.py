import logging
import asyncio
import math
import time
from naptha_sdk.user import sign_consumer_id
from naptha_sdk.modules.agent import Agent
from naptha_sdk.schemas import OrchestratorRunInput, OrchestratorDeployment, AgentRunInput
from keynesian_beauty_contest.schemas import InputSchema
from typing import Dict

logger = logging.getLogger(__name__)

class KeynesianBeautyContest:
    """Keynesian beauty contest orchestrator implementation"""
    def __init__(self, orchestrator_deployment: OrchestratorDeployment, *args, **kwargs):
        self.orchestrator_deployment = orchestrator_deployment
        self.agent_deployments = self.orchestrator_deployment.agent_deployments
        
    async def run_beauty_contest(self, module_run: OrchestratorRunInput, *args, **kwargs):
        num_nodes = len(self.agent_deployments)
        num_agents = int(module_run.inputs.num_agents)
        agents_per_node = math.ceil(num_agents / num_nodes)

        ist = time.time()
        logger.info(f"Running {num_agents} agents...")
        
        tasks = []
        for i in range(num_agents):
            node_index = min(i // agents_per_node, num_nodes - 1)
            name = f"Agent_{i}"

            agent_run_input = AgentRunInput(
                consumer_id=module_run.consumer_id,
                inputs={"agent_name": name},
                deployment=self.agent_deployments[node_index],
                signature=sign_consumer_id(module_run.consumer_id, os.getenv("PRIVATE_KEY"))
            )
            
            agent = Agent(
                deployment=self.agent_deployments[node_index],
            )
            tasks.append(agent.call_agent_func(agent_run_input))

        results = await asyncio.gather(*tasks)
        
        iet = time.time()
        logger.info(f"[Run time: {iet - ist} s]")

        logger.info(f"Results: {results}")
        results = [result.results[0] for result in results]
        logger.info(f"Final results: {results}")

        return results

async def run(module_run: Dict, *args, **kwargs):
    """Run the Keynesian beauty contest between multiple agents."""
    module_run = OrchestratorRunInput(**module_run)
    module_run.inputs = InputSchema(**module_run.inputs)
    beauty_contest = KeynesianBeautyContest(module_run.deployment)
    results = await beauty_contest.run_beauty_contest(module_run, *args, **kwargs)
    return results

if __name__ == "__main__":
    from naptha_sdk.client.naptha import Naptha
    from naptha_sdk.configs import setup_module_deployment
    from naptha_sdk.user import sign_consumer_id
    import os

    naptha = Naptha()

    deployment = asyncio.run(setup_module_deployment(
        "orchestrator", 
        "keynesian_beauty_contest/configs/deployment.json", 
        node_url=os.getenv("NODE_URL")
    ))

    input_params = {"num_agents": 10}  # Example input
        
    module_run = {
        "inputs": input_params,
        "deployment": deployment,
        "consumer_id": naptha.user.id,
        "signature": sign_consumer_id(naptha.user.id, os.getenv("PRIVATE_KEY"))
    }

    # Run the orchestration
    response = asyncio.run(run(module_run))
    print(response)