import Foundation

func runPythonScript(_ scriptName: String, arguments: [String]) -> String {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
    
    let scriptPath = Bundle.main.path(forResource: scriptName, ofType: "py")!
    process.arguments = [scriptPath] + arguments

    let pipe = Pipe()
    process.standardOutput = pipe
    process.standardError = pipe

    do {
        try process.run()
        process.waitUntilExit()
        
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        return String(data: data, encoding: .utf8) ?? ""
    } catch {
        return "Error: \(error.localizedDescription)"
    }
}

func checkPythonEnvironment() -> Bool {
    let pythonCheck = Process()
    pythonCheck.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
    pythonCheck.arguments = ["-c", "import requests, PIL, pytesseract"]

    do {
        try pythonCheck.run()
        pythonCheck.waitUntilExit()
        return pythonCheck.terminationStatus == 0
    } catch {
        print("Error checking Python environment: \(error.localizedDescription)")
        return false
    }
}

func installRequirements() -> Bool {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: "/usr/bin/pip3")
    
    let requirementsPath = Bundle.main.path(forResource: "requirements", ofType: "txt")!
    process.arguments = ["install", "-r", requirementsPath]

    do {
        try process.run()
        process.waitUntilExit()
        return process.terminationStatus == 0
    } catch {
        print("Error installing requirements: \(error.localizedDescription)")
        return false
    }
}

let listener = NSXPCListener.service()
let delegate = HelperToolDelegate()
listener.delegate = delegate
listener.resume()

class HelperToolDelegate: NSObject, NSXPCListenerDelegate {
    func listener(_ listener: NSXPCListener, shouldAcceptNewConnection newConnection: NSXPCConnection) -> Bool {
        newConnection.exportedInterface = NSXPCInterface(with: HelperToolProtocol.self)
        let exportedObject = HelperTool()
        newConnection.exportedObject = exportedObject
        newConnection.resume()
        return true
    }
}

@objc protocol HelperToolProtocol {
    func processDirectory(_ path: String, apiKey: String, reply: @escaping (String) -> Void)
    func indexFiles(_ path: String, apiKey: String, reply: @escaping (String) -> Void)
    func checkPythonEnvironment(reply: @escaping (Bool) -> Void)
    func installRequirements(reply: @escaping (Bool) -> Void)
}

class HelperTool: NSObject, HelperToolProtocol {
    func processDirectory(_ path: String, apiKey: String, reply: @escaping (String) -> Void) {
        let output = runPythonScript("process_images", arguments: [path, apiKey])
        reply(output)
    }
    
    func indexFiles(_ path: String, apiKey: String, reply: @escaping (String) -> Void) {
        let output = runPythonScript("index_files", arguments: [path, apiKey])
        reply(output)
    }
    
    func checkPythonEnvironment(reply: @escaping (Bool) -> Void) {
        reply(checkPythonEnvironment())
    }
    
    func installRequirements(reply: @escaping (Bool) -> Void) {
        reply(installRequirements())
    }
}
