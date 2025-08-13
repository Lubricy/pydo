from functional.do import Bind, Pure, do


@do
def workflow(bind: Bind, pure: Pure):
    prompt = bind(read_prompt())
    response = bind(llm(prompt))


    return pure(())
