from pathlib import Path

HOSTS_PATH = Path("/etc/hosts")
HOSTS_MARKER = "# === Huginn ==="

MONITOR_INTERVAL = 5

AI_DOMAINS: tuple[str, ...] = (
    # OpenAI
    "chatgpt.com",
    "openai.com",
    "chat.openai.com",
    # Anthropic
    "claude.ai",
    "anthropic.com",
    # Google AI
    "gemini.google.com",
    "bard.google.com",
    "aistudio.google.com",
    "labs.google",
    "notebooklm.google",
    # Microsoft
    "copilot.microsoft.com",
    "copilot.cloud.microsoft",
    "bing.com/chat",
    # Meta
    "ai.meta.com",
    "llama.meta.com",
    # Mistral
    "mistral.ai",
    "chat.mistral.ai",
    # DeepSeek
    "deepseek.com",
    "chat.deepseek.com",
    # Image generation
    "midjourney.com",
    "stability.ai",
    "leonardo.ai",
    "civitai.com",
    "ideogram.ai",
    "flux1.ai",
    "dalle.com",
    # Other AI services
    "perplexity.ai",
    "you.com",
    "assistant.you.com",
    "phind.com",
    "poe.com",
    "character.ai",
    "huggingface.co",
    "huggingface.co/chat",
    "together.ai",
    "groq.com",
    "groq.com/playground",
    "cohere.com",
    "kimi.moonshot.cn",
    "reka.ai",
)

AI_PROCESS_NAMES: tuple[str, ...] = (
    # LLM runners
    "ollama",
    "ollama-linux",
    "ollama-serve",
    "llama.cpp",
    "llama-server",
    "llama-cli",
    "llamacpp",
    "vllm",
    "text-generation-inference",
    "triton",
    # Web UIs
    "text-generation-webui",
    "textgen",
    "lmstudio",
    "lm-studio",
    "gpt4all",
    "gpt4all-chat",
    "koboldcpp",
    "kobold",
    "localai",
    "jan",
    "january",
    "nomic",
    "siliconflow",
    # Image generation
    "stable-diffusion-webui",
    "webui",
    "comfyui",
    "comfy",
    "automatic1111",
    "invokeai",
    "drawthings",
    # AI assistants
    "open-interpreter",
    "aider",
    "continue",
    "tabby",
)

AI_PROCESS_CMDLINE: tuple[str, ...] = (
    "ollama",
    "llama.cpp",
    "llama-server",
    "text-generation",
    "stable-diffusion",
    "comfyui",
    "automatic1111",
    "gpt4all",
    "kobold",
    "lmstudio",
    "open-interpreter",
)
