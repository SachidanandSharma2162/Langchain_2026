from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

splitter=RecursiveCharacterTextSplitter.from_language(
    language=Language.JAVA,
    chunk_size=100,
    chunk_overlap=0
)


text="""
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyController {

    @GetMapping("/hello")
    public String helloRoute() {
        return "Hello, World!";
    }
}"""

res=splitter.split_text(text)

print(res)