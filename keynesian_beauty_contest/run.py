#!/usr/bin/env python
import asyncio
import math
from naptha_sdk.client.node import Node
from naptha_sdk.schemas import AgentRunInput
from naptha_sdk.task import Task as Agent
from naptha_sdk.utils import get_logger, load_yaml
from keynesian_beauty_contest.schemas import InputSchema
import time

logger = get_logger(__name__)

async def run_agent(agent, name):
    response = await agent(agent_name=name)
    return response

async def run(inputs, worker_nodes=None, orchestrator_node=None, flow_run=None, cfg=None):
    logger.info(f"Inputs: {inputs}")

    num_nodes = len(worker_nodes)
    num_agents = inputs.num_agents
    agents_per_node = math.ceil(num_agents / num_nodes)

    ist = time.time()
    logger.info(f"Running {num_agents} agents...")
    tasks = []
    results = []
    for i in range(num_agents):
        node_index = min(i // agents_per_node, num_nodes - 1)
        name = f"Agent_{i}"
        agent = Agent(name=name, fn="random_number_agent", worker_node=worker_nodes[node_index], orchestrator_node=orchestrator_node, flow_run=flow_run)
        tasks.append(run_agent(agent, name))

    results = await asyncio.gather(*tasks)

    iet = time.time()
    logger.info(f"[Run time: {iet - ist} s]")

    logger.info(f"Results: {results}")

    return results 


if __name__ == "__main__":
    cfg_path = "keynesian_beauty_contest/component.yaml"
    cfg = load_yaml(cfg_path)

    inputs = {
        "num_agents": 2,
    }
    flow_run = {"consumer_id": "user:18837f9faec9a02744d308f935f1b05e8ff2fc355172e875c24366491625d932f36b34a4fa80bac58db635d5eddc87659c2b3fa700a1775eb4c43da6b0ec270d", 
                "agent_name": "random_agent", "agent_source_url": "https://github.com/NapthaAI/keynesian_beauty_contest", "agent_version": "0.1", "worker_nodes": ["http://localhost:7001"]} 
    flow_run = AgentRunInput(**flow_run)
    inputs = InputSchema(**inputs)
    orchestrator_node = Node("http://localhost:7001")
    worker_nodes = [Node(worker_node) for worker_node in flow_run.worker_nodes]

    response = asyncio.run(run(inputs, worker_nodes, orchestrator_node, flow_run, cfg))
    print(response)
    print("Flow Run: ", flow_run)