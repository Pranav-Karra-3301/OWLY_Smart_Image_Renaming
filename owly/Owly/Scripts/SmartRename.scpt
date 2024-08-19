on run {input, parameters}
    
    -- Get API Key from parameters
    set apiKey to item 1 of parameters
    
    -- Function to encode image to base64
    on encodeImage(filePath)
        set cmd to "base64 -i " & quoted form of filePath & " | tr -d '\n'"
        set encodedImage to do shell script cmd
        return encodedImage
    end encodeImage
    
    -- Function to generate smart filename using OpenAI API
    on generateSmartFilename(base64Image, originalFilename)
        set system_prompt to "You are an AI trained to generate concise, context-aware filenames for images. Create a filename that accurately describes the image content, considering these guidelines:

1. If it's a scene from a movie, TV show, or features a celebrity, include the relevant name.
2. For math content, include 'Math' and specify (e.g., Calculus, Algebra).
3. For code or programming, include 'Code' and the language (e.g., Python, Java).
4. For chat screenshots, include 'Chat' and the platform (e.g., WhatsApp, Instagram, Discord, Slack).
5. For website screenshots, include 'Website' and the site name (e.g., Google, Facebook).
6. For graphs, include 'Graph' and the type (e.g., Bar Graph, Line Graph).

Keep the filename under 150 characters, but make it specific and descriptive. Capture the essence of the image or file."

        set curlCmd to "curl https://api.openai.com/v1/chat/completions " & ¬
            "-H \"Content-Type: application/json\" " & ¬
            "-H \"Authorization: Bearer " & apiKey & "\" " & ¬
            "-d '{\"model\": \"gpt-4o\", " & ¬
            "\"messages\": [{\"role\": \"system\", \"content\": \"" & system_prompt & "\"}, " & ¬
            "{\"role\": \"user\", \"content\": [{\"type\": \"image_url\", \"image_url\": {\"url\": \"data:image/jpeg;base64," & base64Image & "\"}}]}], " & ¬
            "\"max_tokens\": 300}'"
        
        set apiResponse to do shell script curlCmd
        set AppleScript's text item delimiters to {"\"content\":\"", "\"}"}
        set newFilename to text item 2 of apiResponse
        set AppleScript's text item delimiters to {""}
        
        return newFilename
    end generateSmartFilename
    
    -- Main logic
    repeat with filePath in input
        set originalFilename to name of (info for filePath)
        set base64Image to encodeImage(filePath)
        set newFilename to generateSmartFilename(base64Image, originalFilename)
        
        -- Rename the file
        tell application "Finder"
            set name of file filePath to newFilename
        end tell
        
        log "Renamed " & originalFilename & " to " & newFilename
    end repeat
    
    return input
end run
