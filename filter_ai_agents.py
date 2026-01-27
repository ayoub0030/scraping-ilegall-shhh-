import json

def filter_ai_agents(input_file, output_file):
    """Filter projects that are specifically about AI agents"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    
    ai_agent_keywords = [
        'agent', 'agents', 'autonomous', 'assistant', 'chatbot', 'bot',
        'conversational', 'dialogue', 'nlp', 'natural language', 'llm',
        'large language model', 'gpt', 'claude', 'gemini', 'ai assistant',
        'virtual assistant', 'intelligent agent', 'ai agent', 'multi-agent'
    ]
    
    filtered_projects = []
    
    for project in projects:
        title_lower = project['title'].lower()
        tagline_lower = project['tagline'].lower()
        
        # Check if project mentions AI agents
        is_ai_agent = any(keyword in title_lower or keyword in tagline_lower 
                         for keyword in ai_agent_keywords)
        
        if is_ai_agent:
            filtered_projects.append(project)
    
    print(f"Original projects: {len(projects)}")
    print(f"AI agent projects: {len(filtered_projects)}")
    
    # Save filtered results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_projects, f, indent=4, ensure_ascii=False)
    
    # Show some examples
    print(f"\nFirst 10 AI agent projects:")
    for i, project in enumerate(filtered_projects[:10]):
        print(f"{i+1}. {project['title']}")
        print(f"   {project['tagline']}")
        print(f"   {project['url']}")
        print()
    
    return filtered_projects

if __name__ == "__main__":
    filter_ai_agents('devpost_projects_all.json', 'ai_agents_projects.json')
