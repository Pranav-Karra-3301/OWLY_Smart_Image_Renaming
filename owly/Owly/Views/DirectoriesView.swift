import SwiftUI
import Foundation

struct WatchedDirectory: Identifiable, Codable {
    let id: UUID
    let path: String
    var isWatched: Bool
    var lastProcessedTimestamp: Date?
}

class DirectoryWatcher: ObservableObject {
    private var watchers: [String: DispatchSourceFileSystemObject] = [:]
    
    func startWatching(_ path: String, callback: @escaping () -> Void) {
        let fileDescriptor = open(path, O_EVTONLY)
        guard fileDescriptor >= 0 else { return }
        
        let source = DispatchSource.makeFileSystemObjectSource(fileDescriptor: fileDescriptor, eventMask: .write, queue: .main)
        source.setEventHandler {
            callback()
        }
        source.setCancelHandler {
            close(fileDescriptor)
        }
        source.resume()
        
        watchers[path] = source
    }
    
    func stopWatching(_ path: String) {
        watchers[path]?.cancel()
        watchers.removeValue(forKey: path)
    }
}

@objc protocol HelperToolProtocol {
    func processDirectory(_ path: String, apiKey: String, reply: @escaping (String) -> Void)
    func indexFiles(_ path: String, apiKey: String, reply: @escaping (String) -> Void)
    func checkPythonEnvironment(reply: @escaping (Bool) -> Void)
    func installRequirements(reply: @escaping (Bool) -> Void)
}

class DirectoriesViewModel: ObservableObject {
    @Published var directories: [WatchedDirectory] = []
    @Published var processingProgress: Double = 0
    @Published var indexingProgress: Double = 0
    @Published var unprocessedImageCount: Int = 0
    @Published var isPythonEnvironmentReady: Bool = false
    @Published var isInstallingRequirements: Bool = false
    private let watcher = DirectoryWatcher()
    private var helperConnection: NSXPCConnection?
    
    init() {
        setupHelperConnection()
        loadDirectories()
        if directories.isEmpty {
            addDefaultDirectories()
        }
        checkPythonEnvironment()
    }
    
    private func setupHelperConnection() {
        helperConnection = NSXPCConnection(serviceName: "com.yourcompany.OwlyHelper")
        helperConnection?.remoteObjectInterface = NSXPCInterface(with: HelperToolProtocol.self)
        helperConnection?.resume()
    }
    
    func checkPythonEnvironment() {
        guard let helper = helperConnection?.remoteObjectProxy as? HelperToolProtocol else {
            print("Failed to get helper proxy")
            return
        }
        
        helper.checkPythonEnvironment { result in
            DispatchQueue.main.async {
                self.isPythonEnvironmentReady = result
            }
        }
    }
    
    func installRequirements() {
        guard let helper = helperConnection?.remoteObjectProxy as? HelperToolProtocol else {
            print("Failed to get helper proxy")
            return
        }
        
        isInstallingRequirements = true
        helper.installRequirements { result in
            DispatchQueue.main.async {
                self.isInstallingRequirements = false
                self.isPythonEnvironmentReady = result
                if result {
                    print("Requirements installed successfully")
                } else {
                    print("Failed to install requirements")
                }
            }
        }
    }
    
    func addDefaultDirectories() {
        let screenshotsPath = FileManager.default.urls(for: .picturesDirectory, in: .userDomainMask).first!.appendingPathComponent("Screenshots").path
        directories.append(WatchedDirectory(id: UUID(), path: screenshotsPath, isWatched: false))
        saveDirectories()
    }
    
    func addDirectory(_ path: String) {
        let newDirectory = WatchedDirectory(id: UUID(), path: path, isWatched: false)
        directories.append(newDirectory)
        saveDirectories()
    }
    
    func toggleWatching(_ directory: WatchedDirectory) {
        if let index = directories.firstIndex(where: { $0.id == directory.id }) {
            directories[index].isWatched.toggle()
            if directories[index].isWatched {
                startWatching(directories[index])
            } else {
                stopWatching(directories[index])
            }
            saveDirectories()
        }
    }
    
    private func startWatching(_ directory: WatchedDirectory) {
        watcher.startWatching(directory.path) {
            self.processNewFiles(in: directory)
        }
    }
    
    private func stopWatching(_ directory: WatchedDirectory) {
        watcher.stopWatching(directory.path)
    }
    
    func reloadDirectory(_ directory: WatchedDirectory) {
        processFiles(in: directory)
    }
    
    private func processNewFiles(in directory: WatchedDirectory) {
        processFiles(in: directory)
    }
    
    private func processFiles(in directory: WatchedDirectory) {
        guard isPythonEnvironmentReady else {
            print("Python environment is not ready")
            return
        }
        
        guard let helper = helperConnection?.remoteObjectProxy as? HelperToolProtocol else {
            print("Failed to get helper proxy")
            return
        }
        
        let apiKey = KeychainHelper.shared.retrieve(key: "openai_api_key") ?? ""
        
        helper.processDirectory(directory.path, apiKey: apiKey) { output in
            print("Processing output: \(output)")
            DispatchQueue.main.async {
                self.updateProgress(output: output)
            }
        }
        
        helper.indexFiles(directory.path, apiKey: apiKey) { output in
            print("Indexing output: \(output)")
            DispatchQueue.main.async {
                self.updateIndexingProgress(output: output)
            }
        }
    }
    
    private func updateProgress(output: String) {
        let lines = output.split(separator: "\n")
        for line in lines {
            if line.starts(with: "PROGRESS:"), let progress = Double(line.split(separator: ":")[1]) {
                self.processingProgress = progress
            } else if line.starts(with: "UNPROCESSED:"), let count = Int(line.split(separator: ":")[1]) {
                self.unprocessedImageCount = count
            }
        }
    }
    
    private func updateIndexingProgress(output: String) {
        if let progressLine = output.split(separator: "\n").first(where: { $0.starts(with: "PROGRESS:") }),
           let progress = Double(progressLine.split(separator: ":")[1]) {
            self.indexingProgress = progress
        }
    }
    
    func loadDirectories() {
        if let data = UserDefaults.standard.data(forKey: "watchedDirectories"),
           let decoded = try? JSONDecoder().decode([WatchedDirectory].self, from: data) {
            directories = decoded
            for directory in directories where directory.isWatched {
                startWatching(directory)
            }
        }
    }
    
    func saveDirectories() {
        if let encoded = try? JSONEncoder().encode(directories) {
            UserDefaults.standard.set(encoded, forKey: "watchedDirectories")
        }
    }
}

struct DirectoriesView: View {
    @StateObject private var viewModel = DirectoriesViewModel()
    @State private var isAddingDirectory = false
    @State private var showingPythonAlert = false
    
    var body: some View {
        VStack {
            if !viewModel.isPythonEnvironmentReady {
                Text("Python environment is not ready")
                    .foregroundColor(.red)
                Button("Install Requirements") {
                    viewModel.installRequirements()
                }
                .disabled(viewModel.isInstallingRequirements)
            }
            
            List {
                ForEach(viewModel.directories) { directory in
                    HStack {
                        Image(systemName: "folder")
                            .foregroundColor(.blue)
                        Text(directory.path)
                        Spacer()
                        Button(action: {
                            viewModel.toggleWatching(directory)
                        }) {
                            Image(systemName: directory.isWatched ? "eye.fill" : "eye.slash.fill")
                        }
                        .buttonStyle(PlainButtonStyle())
                        
                        Button(action: {
                            if viewModel.isPythonEnvironmentReady {
                                viewModel.reloadDirectory(directory)
                            } else {
                                showingPythonAlert = true
                            }
                        }) {
                            Image(systemName: "arrow.clockwise")
                        }
                        .buttonStyle(PlainButtonStyle())
                    }
                }
                .onDelete(perform: deleteDirectories)
            }
            .listStyle(SidebarListStyle())
            
            Button("Add Directory") {
                isAddingDirectory = true
            }
            .padding()
        }
        .fileImporter(isPresented: $isAddingDirectory, allowedContentTypes: [.folder]) { result in
            switch result {
            case .success(let url):
                viewModel.addDirectory(url.path)
            case .failure(let error):
                print("Error selecting directory: \(error.localizedDescription)")
            }
        }
        .alert(isPresented: $showingPythonAlert) {
            Alert(
                title: Text("Python Environment Not Ready"),
                message: Text("Please install the required Python libraries before processing directories."),
                primaryButton: .default(Text("Install Now")) {
                    viewModel.installRequirements()
                },
                secondaryButton: .cancel()
            )
        }
    }
    
    private func deleteDirectories(at offsets: IndexSet) {
        for index in offsets {
            let directory = viewModel.directories[index]
            if directory.isWatched {
                viewModel.toggleWatching(directory)
            }
        }
        viewModel.directories.remove(atOffsets: offsets)
        viewModel.saveDirectories()
    }
}

struct DirectoriesView_Previews: PreviewProvider {
    static var previews: some View {
        DirectoriesView()
    }
}
