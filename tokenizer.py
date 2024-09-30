import tiktoken


tokenizer =  tiktoken.encoding_for_model("gpt-3.5-turbo")
print(tokenizer.name)


# 分词得到向量
res = tokenizer.encode("tiktoken world")
print(res)
print(len(res))


# 向量还原文本
print(tokenizer.decode(res))

# 把每一个整数还原成一个词条
words = [tokenizer.decode_single_token_bytes(token) for token in res]
print(words)
