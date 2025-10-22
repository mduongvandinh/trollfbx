# backend/app/services/meme_analyzer_service.py
"""
Meme Analyzer Service
Uses AI to analyze meme images and extract patterns for reuse
"""
import json
import base64
from typing import Dict, List, Optional
from pathlib import Path
import requests


class MemeAnalyzerService:
    """Service to analyze meme images using AI"""

    def __init__(self):
        from app.services.ai_content_service_ollama import AIContentGenerator
        self.ai_generator = AIContentGenerator()
        self.ollama_url = "http://localhost:11434"

    def analyze_meme_text(
        self,
        caption: str,
        context: Optional[str] = None
    ) -> Dict:
        """
        Analyze meme caption to understand template and humor pattern

        Args:
            caption: The meme caption/text
            context: Additional context about the meme

        Returns:
            Dict with analysis results
        """
        try:
            analysis_prompt = f"""Phân tích caption meme bóng đá này:

Caption: "{caption}"
{f'Context: {context}' if context else ''}

Trả lời JSON:
{{
    "template_type": "loại template (vd: childhood_dream_irony, sponsor_troll, trophy_banter, etc.)",
    "humor_type": "kiểu hài hước (irony, sarcasm, exaggeration, disappointment, etc.)",
    "key_elements": ["yếu tố chính 1", "yếu tố chính 2"],
    "football_context": {{
        "player": "tên cầu thủ nếu có",
        "team": "đội bóng nếu có",
        "situation": "tình huống"
    }},
    "reusable_format": "mô tả cấu trúc template để tái sử dụng",
    "pattern": "công thức chung của meme này"
}}"""

            # Call AI to analyze
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "qwen2.5:7b-instruct-q4_K_M",
                    "prompt": analysis_prompt,
                    "temperature": 0.3,
                    "stream": False
                },
                timeout=30
            )

            result = response.json()
            ai_response = result.get("response", "")

            # Try to parse JSON
            try:
                # Extract JSON from response
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = ai_response[json_start:json_end]
                    analysis = json.loads(json_str)
                else:
                    raise ValueError("No JSON found")
            except:
                # Fallback structure
                analysis = {
                    "template_type": "unknown",
                    "humor_type": "unknown",
                    "key_elements": [],
                    "football_context": {},
                    "reusable_format": ai_response,
                    "pattern": ""
                }

            return analysis

        except Exception as e:
            print(f"Error analyzing meme text: {str(e)}")
            return {
                "error": str(e),
                "template_type": "error",
                "description": f"Failed to analyze: {str(e)}"
            }

    def generate_caption_variations(
        self,
        template_analysis: Dict,
        player_name: Optional[str] = None,
        context: Optional[str] = None,
        num_variations: int = 10
    ) -> List[str]:
        """
        Generate new caption variations based on template analysis

        Args:
            template_analysis: Analysis dict from analyze_meme_image()
            player_name: Player to use in new captions (optional)
            context: Specific context/situation (optional)
            num_variations: Number of variations to generate

        Returns:
            List of caption variations
        """
        try:
            # Build generation prompt
            template_format = template_analysis.get("reusable_format", "")
            humor_type = template_analysis.get("humor_type", "")
            template_type = template_analysis.get("template_type", "")

            generation_prompt = f"""Based on this meme template analysis:

Template Type: {template_type}
Humor Type: {humor_type}
Format: {template_format}

Original Caption: {template_analysis.get('caption', '')}

Generate {num_variations} NEW caption variations following the same format and humor style.
"""

            if player_name:
                generation_prompt += f"\nUse player: {player_name}"
            if context:
                generation_prompt += f"\nContext: {context}"

            generation_prompt += f"""

Rules:
- Follow the same meme format/structure
- Use the same type of humor ({humor_type})
- Make it relevant to football
- Be creative and funny
- Each caption should be unique

Return ONLY a JSON array of captions:
["caption 1", "caption 2", "caption 3", ...]
"""

            response = self.ollama.generate(
                prompt=generation_prompt,
                temperature=0.8  # Higher temperature for creativity
            )

            # Parse JSON array
            try:
                variations = json.loads(response)
                if isinstance(variations, list):
                    return variations[:num_variations]
                else:
                    return [response]
            except json.JSONDecodeError:
                # Split by newlines if not JSON
                return [line.strip() for line in response.split('\n') if line.strip()][:num_variations]

        except Exception as e:
            print(f"Error generating variations: {str(e)}")
            return [f"Error: {str(e)}"]

    def extract_meme_categories(self, analysis_list: List[Dict]) -> Dict[str, int]:
        """
        Analyze multiple memes to identify common categories

        Args:
            analysis_list: List of meme analysis dicts

        Returns:
            Dict of category: count
        """
        categories = {}
        for analysis in analysis_list:
            template_type = analysis.get("template_type", "unknown")
            categories[template_type] = categories.get(template_type, 0) + 1

        return categories

    def suggest_players_for_template(
        self,
        template_analysis: Dict,
        num_suggestions: int = 5
    ) -> List[Dict]:
        """
        Suggest football players that would fit this meme template

        Args:
            template_analysis: Meme template analysis
            num_suggestions: Number of player suggestions

        Returns:
            List of player suggestions with reasoning
        """
        template_type = template_analysis.get("template_type", "")
        humor_type = template_analysis.get("humor_type", "")
        original_context = template_analysis.get("football_context", {})

        prompt = f"""Based on this meme template:

Type: {template_type}
Humor: {humor_type}
Original Context: {json.dumps(original_context, indent=2)}

Suggest {num_suggestions} football players who would fit this meme format perfectly.

For each player, explain:
- Why they fit this template
- What situation/context would work
- Example caption

Return JSON array:
[
    {{
        "player": "Player Name",
        "team": "Current Team",
        "reason": "Why they fit",
        "situation": "Specific situation/context",
        "example_caption": "Example meme caption"
    }},
    ...
]
"""

        try:
            response = self.ollama.generate(prompt=prompt, temperature=0.7)
            suggestions = json.loads(response)
            return suggestions if isinstance(suggestions, list) else []
        except Exception as e:
            print(f"Error suggesting players: {str(e)}")
            return []


# Global instance
meme_analyzer_service = MemeAnalyzerService()
