using System.Net.Http.Json;

var httpClient = new HttpClient();

// 1. Pack the parcel
var request = new PromptRequest { Prompt = "Say hello in 3 languages" };

// 2. Send it to FastAPI
var response = await httpClient.PostAsJsonAsync(
    "http://127.0.0.1:8000/generate", request);

// 3. Open the reply
if (response.IsSuccessStatusCode)
{
    var result = await response.Content.ReadFromJsonAsync<PromptResponse>();
    Console.WriteLine("Gemini says: " + result?.Answer);
}
else
{
    Console.WriteLine("Error: " + await response.Content.ReadAsStringAsync());
}

// Models stay at the very bottom
public class PromptRequest
{
    public string Prompt { get; set; } = string.Empty;
}

public class PromptResponse
{
    public string Answer { get; set; } = string.Empty;
}