#!/usr/bin/env python
import asyncio
from concurrent import futures
from concurrent.futures import as_completed
import math
from naptha_sdk.client.node import Node
from naptha_sdk.schemas import ModuleRunInput
from naptha_sdk.task import Task as Agent
from naptha_sdk.utils import get_logger, load_yaml
from random_number_protocol.schemas import InputSchema
import time

logger = get_logger(__name__)

async def run_agent(agent):
    response = await agent()
    return response

def run(inputs, worker_nodes=None, orchestrator_node=None, flow_run=None, cfg=None):
    logger.info(f"Inputs: {inputs}")

    num_nodes = len(worker_nodes)
    num_agents = inputs.num_agents
    agents_per_node = math.ceil(num_agents / num_nodes)

    ist = time.time()
    logger.info(f"Running {num_agents} agents...")
    tasks = []
    results = []
    with futures.ThreadPoolExecutor(max_workers=None) as executor:
        for i in range(num_agents):
            node_index = min(i // agents_per_node, num_nodes - 1)
            agent = Agent(name=f"Agent_{i}", fn="random_number_agent", worker_node=worker_nodes[node_index], orchestrator_node=orchestrator_node, flow_run=flow_run)

            tasks.append(
                executor.submit(
                    run_agent,
                    agent
                ),
            )
        for task in as_completed(tasks):
            results.append(task.result())

    iet = time.time()
    logger.info(f"[init takes {iet - ist} s]")

    # run te
    st = time.time()
    results2 = []
    for p in results:
        results2.append(p())
    summ = 0
    cnt = 0
    for r in results2:
        try:
            summ += int(r.content["sum"])
            cnt += int(r.content["cnt"])
        except Exception:
            logger.error(r.content)
    et = time.time()
    logger.info(f"The average value is {summ/cnt} [takes {et-st} s]")


if __name__ == "__main__":
    cfg_path = "random_number_protocol/component.yaml"
    cfg = load_yaml(cfg_path)

    inputs = {
        "num_agents": 2,
    }
    flow_run = {"consumer_id": "user:18837f9faec9a02744d308f935f1b05e8ff2fc355172e875c24366491625d932f36b34a4fa80bac58db635d5eddc87659c2b3fa700a1775eb4c43da6b0ec270d", 
                "module_name": "random_number_protocol", "module_type": "flow", "worker_nodes": ["http://localhost:7001"]}
    flow_run = ModuleRunInput(**flow_run)
    inputs = InputSchema(**inputs)
    orchestrator_node = Node("http://localhost:7001")
    worker_nodes = [Node(worker_node) for worker_node in flow_run.worker_nodes]

    response = asyncio.run(run(inputs, worker_nodes, orchestrator_node, flow_run, cfg))
    print(response)
    print("Flow Run: ", flow_run)