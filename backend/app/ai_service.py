from __future__ import annotations

import os

from openai import OpenAI


class AIService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def rewrite_content(self, content: str, focus_keyword: str, tone: str) -> str:
        prompt = (
            "Rewrite the following content in a natural, human tone while improving SEO. "
            f"Primary keyword: {focus_keyword}. Tone: {tone}. Keep the meaning accurate, "
            "make it more readable, and include semantic keyword variations.\n\n"
            f"Content:\n{content}"
        )
        return self._generate(prompt, fallback=self._fallback_rewrite(content, focus_keyword))

    def generate_keywords(self, topic: str, seed_keywords: list[str]) -> list[str]:
        seed_text = ", ".join(seed_keywords) if seed_keywords else "none"
        prompt = (
            "Generate 25 SEO keyword ideas (short-tail + long-tail) for the topic below. "
            "Return each keyword on a new line only.\n\n"
            f"Topic: {topic}\nSeed keywords: {seed_text}"
        )
        text = self._generate(prompt, fallback=self._fallback_keywords(topic, seed_keywords))
        return [line.strip("- ").strip() for line in text.splitlines() if line.strip()]

    def generate_blog(self, topic: str, target_keyword: str, audience: str) -> str:
        prompt = (
            "Write a complete SEO-optimized blog post with: title, intro, H2 sections, "
            "actionable insights, and a conclusion. Use markdown headings. "
            f"Topic: {topic}. Target keyword: {target_keyword}. Audience: {audience}."
        )
        fallback = (
            f"# {topic}: Practical Guide\n\n"
            f"Target keyword: {target_keyword}\n\n"
            "## Why This Matters\n"
            "This topic has strong search intent and can attract consistent organic traffic.\n\n"
            "## Key Strategies\n"
            "1. Build content around user intent.\n"
            "2. Optimize headings and metadata.\n"
            "3. Add internal links and relevant examples.\n\n"
            "## Conclusion\n"
            "Keep content helpful, structured, and keyword-aligned for long-term SEO growth."
        )
        return self._generate(prompt, fallback=fallback)

    def _generate(self, prompt: str, fallback: str) -> str:
        if not self.client:
            return fallback
        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                temperature=0.7,
            )
            return (response.output_text or "").strip() or fallback
        except Exception:
            return fallback

    def _fallback_rewrite(self, content: str, focus_keyword: str) -> str:
        return (
            f"{content}\n\n"
            f"Optimized version note: naturally include '{focus_keyword}' in headings, intros, and CTA text."
        )

    def _fallback_keywords(self, topic: str, seed_keywords: list[str]) -> str:
        seed = seed_keywords[:5]
        base = [
            topic,
            f"{topic} guide",
            f"best {topic}",
            f"{topic} tips",
            f"{topic} strategy",
            f"{topic} checklist",
            f"{topic} for beginners",
            f"advanced {topic}",
            f"{topic} examples",
            f"{topic} optimization",
            f"{topic} services",
            f"{topic} tools",
            f"{topic} automation",
            f"{topic} trends",
            f"{topic} mistakes",
            f"{topic} best practices",
        ]
        base.extend(seed)
        return "\n".join(dict.fromkeys(base))

