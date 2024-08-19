import SwiftUI
import Combine

struct WatchedDirectory: Identifiable, Codable {
    let id = UUID()
    let path: String
    var isWatched: Bool
}

class DirectoryWatcher {
    private var cancellables = Set<AnyCancellable>()
    
    func startWatching(_ path: String, callback: @escaping () -> Void) {
        let fileManager = FileManager.default
        let queue = DispatchQueue(label: "DirectoryWatcher", attributes: .concurrent)
        
        queue.async {
            while true {
                let enumerator = fileManager.enumerator(atPath: path)
                var files = Set<String>()
                while let filePath = enumerator?.nextObject() as? String {
                    files.insert(filePath)
                }
                
                Thread.sleep(forTimeInterval: 1.0)
                
                let newEnumerator = fileManager.enumerator(atPath: path)
                var newFiles = Set<String>()
                while let filePath = newEnumerator?.nextObject() as? String {
                    newFiles.insert(filePath)
                }
                
                if files != newFiles {
                    DispatchQueue.main.async {
                        callback()
                    }
                }
            }
        }
    }
}

class DirectoriesViewModel: ObservableObject {
    @Published var directories: [WatchedDirectory] = []
    @Published var isProcessing = false
    private let directoryWatcher = DirectoryWatcher()

    func addDirectory() {
        let panel = NSOpenPanel()
        panel.canChooseDirectories = true
        panel.canChooseFiles = false
        panel.allowsMultipleSelection = false
        panel.begin { response in
            if response == .OK, let url = panel.url {
                let newDirectory = WatchedDirectory(path: url.path, isWatched: true)
                self.directories.append(newDirectory)
                self.saveDirectories()
                self.startWatching(directory: newDirectory)
            }
        }
    }

    func removeDirectories(at offsets: IndexSet) {
        directories.remove(atOffsets: offsets)
        saveDirectories()
    }

    func loadDirectories() {
        if let savedDirectories = UserDefaults.standard.data(forKey: "watchedDirectories"),
           let decodedDirectories = try? JSONDecoder().decode([WatchedDirectory].self, from: savedDirectories) {
            directories = decodedDirectories
            for directory in directories where directory.isWatched {
                startWatching(directory: directory)
            }
        }
    }

    func saveDirectories() {
        if let encoded = try? JSONEncoder().encode(directories) {
            UserDefaults.standard.set(encoded, forKey: "watchedDirectories")
        }
    }

    func startWatching(directory: WatchedDirectory) {
        directoryWatcher.startWatching(directory.path) {
            self.processFiles(statusViewModel: nil)
        }
    }

    func processFiles(statusViewModel: StatusViewModel?) {
        guard !isProcessing else { return }
        isProcessing = true
        
        let watchedDirectories = directories.filter { $0.isWatched }.map { $0.path }
        
        guard let apiKey = KeychainHelper.shared.retrieve(key: "openai_api_key") else {
            print("API key not found in Keychain")
            isProcessing = false
            return
        }
        
        DispatchQueue.global(qos: .background).async {
            for directory in watchedDirectories {
                let files = self.getFiles(in: directory)
                statusViewModel?.waitingFilesCount += files.count
                self.runAppleScript(with: files, apiKey: apiKey, statusViewModel: statusViewModel)
            }
            
            DispatchQueue.main.async {
                self.isProcessing = false
                statusViewModel?.updateProcessingProgress(1.0)
                NotificationCenter.default.post(name: .newFilesProcessed, object: nil)
            }
        }
    }

    private func getFiles(in directory: String) -> [String] {
        let fileManager = FileManager.default
        guard let enumerator = fileManager.enumerator(atPath: directory) else { return [] }
        
        var files: [String] = []
        while let filePath = enumerator.nextObject() as? String {
            let fullPath = (directory as NSString).appendingPathComponent(filePath)
            if fileManager.isReadableFile(atPath: fullPath) {
                files.append(fullPath)
            }
        }
        return files
    }

    private func runAppleScript(with files: [String], apiKey: String, statusViewModel: StatusViewModel?) {
        guard let scriptURL = Bundle.main.url(forResource: "SmartRename", withExtension: "scpt") else {
            print("AppleScript file not found")
            return
        }
        
        let task = Process()
        task.launchPath = "/usr/bin/osascript"
        task.arguments = [scriptURL.path] + files + [apiKey]
        
        let pipe = Pipe()
        task.standardOutput = pipe
        task.standardError = pipe
        
        do {
            try task.run()
            task.waitUntilExit()
            
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            if let output = String(data: data, encoding: .utf8) {
                print("AppleScript output: \(output)")
            }
            
            statusViewModel?.incrementFinishedFiles()
            statusViewModel?.updateProcessingProgress(Double(statusViewModel?.finishedFilesCount ?? 0) / Double(statusViewModel?.waitingFilesCount ?? 1))
        } catch {
            print("Error running AppleScript: \(error)")
        }
    }
}

extension Notification.Name {
    static let newFilesProcessed = Notification.Name("newFilesProcessed")
}
