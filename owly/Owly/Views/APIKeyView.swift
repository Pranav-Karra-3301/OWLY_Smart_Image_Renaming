import SwiftUI

struct APIKeyView: View {
    @State private var apiKey: String = ""
    @State private var isAdvancedMode: Bool = false

    var body: some View {
        VStack {
            TextField("Enter OpenAI API Key", text: $apiKey)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            Button("Save API Key") {
                saveApiKey(apiKey)
            }
            .padding()

            Toggle(isOn: $isAdvancedMode) {
                Text("Enable Advanced Mode")
            }
            .padding()

            Text(isAdvancedMode ? "Advanced mode is on. Using all features." : "Advanced mode is off. Using basic features.")
                .padding()
        }
        .onAppear {
            loadApiKey()
        }
    }

    func saveApiKey(_ key: String) {
        if KeychainHelper.shared.save(key: "openai_api_key", value: key) {
            print("API Key saved successfully.")
            updateAdvancedMode(apiKey: key)
        } else {
            print("Failed to save API Key.")
        }
    }

    func loadApiKey() {
        if let key = KeychainHelper.shared.retrieve(key: "openai_api_key") {
            apiKey = key
            updateAdvancedMode(apiKey: key)
        }
    }

    func updateAdvancedMode(apiKey: String) {
        isAdvancedMode = !apiKey.isEmpty
        UserDefaults.standard.set(isAdvancedMode, forKey: "advancedMode")
    }
}

struct APIKeyView_Previews: PreviewProvider {
    static var previews: some View {
        APIKeyView()
    }
}
