from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# run search agent

def run_research_pipeline(topic: str)-> dict:
    state = {} # state memory

    # step1: run search agent
    print("\n"+"="*50) # buetefel logs in terminal
    print("step 1: search agent is working........")
    print("="*50) # buetefel logs in terminal

    search_agent=build_search_agent()
    search_result = search_agent.invoke({
    "messages": [
            {
            "role": "user",
            "content": f"Research the following topic and find reliable information: {topic}"
            }
        ]
    })
    state['search_result']= search_result['messages'][-1].content
    print("\n search result", state['search_result'])



    # step 2: run reader agent
    print("\n"+"="*50) # buetefel logs in terminal
    print("step 2: reader agent is working........")
    print("="*50) # buetefel logs in terminal

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
    "messages": [
            {
            "role": "user",
            "content": (
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_result'][:800]}"
                )
            }
        ]   
    })
    state['scraped_content']= reader_result['messages'][-1].content
    print("\nscraped content: \n", state['scraped_content'])


    # step 3: run writer agent
    print("\n"+"="*50) # buetefel logs in terminal
    print("step 3: writer is drafting the report........")
    print("="*50) # buetefel logs in terminal

    research_compines = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
    state['report']= writer_chain.invoke({
        'topic': topic,
        'research': research_compines
    })
    print("\n Final Report\n",state['report'])

    # step 3: run critic  report
    print("\n"+"="*50) # buetefel logs in terminal
    print("step 4: writer is drafting the report........")
    print("="*50) # buetefel logs in terminal
    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })
    print("\n critic report \n", state['feedback'])

    return state

