"""Description of your app."""
from steamship.invocable import Config, post, PackageService




class WriterPackageConfig(Config):
  """Config object containing required parameters to initialize a WriterPackage instance."""

  # This config should match the corresponding configuration in your steamship.json
  default_name: str  = "mipo-gpt-writer-pkg" # Required
  enthusiastic: bool = False  # Not required


class WriterPackage(PackageService):
  """Steamship Package."""

  PROMPT = """

As a content writer use the following parameters to write an article:

Complexity: Low, use high-level vocabularity sparingly
Voice: Active voice
Tone: {tone}
Burstiness: High
Perplexity: High
Target audience: people intrested in {title}
Key takeaway: Highlighted at the end of the article to summarize the main points
Rhetorical questions: Integrated strategically to emphasize key points and engage readers
Figures of speech: Employed selectively to captivate the reader and underscore essential points
Idiomatic expressions: Used sparingly and fittingly to inject personality and convey ideas effectively
Filler words: use selectively filler words.
Structure: {structure}
Number of paragraphs: {paragraphs}
Total length: {min_words} to {max_words} words
Topic: {title}
Comma separated keywords: {keywords}
Changes for readability: Continuously made, focusing on clarity and cohesion, flow, and a seamless reading experience, avoiding repetition
Examples: True
Content Formatting:
- Use bullet points for summarizing key points or listing items
- Bold text for headings
- Headers (H1, H2, H3, etc.) for organizing content into sections and sub-sections
- White space to break up large chunks of text and improve readability
Visual Aids: Suggesting suitable visual elements (images, graphs, charts) to complement the content. Describe images as Dalle-e prompts in brackets.

Regarding generating writing content, two factors are crucial to be in the highest degree, "perplexity" and "burstiness." 
Perplexity measures the complexity of the text. 
Separately, burstiness compares the variations of sentences. 
Humans tend to write with greater burstiness, for example, with some longer or more complex sentences alongside shorter ones. 
Al sentences tend to be more uniform. 
Therefore, generated text content must have the highest degree of perplexity and the highest degree of burstiness. 
The other two factors are that writing should be maximum contextually relevant and maximum coherent.

  """

  # When this package is deployed, this annotation tells Steamship
  # to expose an endpoint that accepts HTTP POST requests for the
  # `/generate` request path.
  # See README.md for more information about deployment.
  @post("generate")
  def generate(self, title: str, keywords: str,min_words: str,max_words: str,tone: str,paragraphs: str,structure: str) -> str:
    """Generate text from prompt parameters."""
    prompt_tokens = 500
    article_tokens = int(max_words) / 0.75
    total_tokens = prompt_tokens + article_tokens
    llm_config = {
      # Controls length of generated output.
      "max_tokens": total_tokens, #GPT-4
      #"max_words": 2000, #GPT-3
      # Controls randomness of output (range: 0.0-1.0).
      "temperature": 0.7
    }
    #gpt-3
    #prompt_args = {"title": title, "keywords": keywords,"min_words":min_words,"max_words":max_words,"tone":tone,"paragraphs":paragraphs,"structure":structure}

    llm = self.client.use_plugin("gpt-4", config=llm_config)
    #gpt-3
    #return llm.generate(self.PROMPT, prompt_args, clean_output=True)
    
    #gpt-4
    task = llm.generate(text=self.PROMPT.format(title=title,keywords=keywords,min_words=min_words,max_words=max_words,tone=tone,paragraphs=paragraphs,structure=structure))
    task.wait(max_timeout_s=600)
    return task.output.blocks[0].text
