import SwiftUI

class StatusViewModel: ObservableObject {
    @Published var processingProgress: Double = 0.0
    @Published var indexingProgress: Double = 0.0
    @Published var waitingFilesCount: Int = 0
    @Published var finishedFilesCount: Int = 0

    func updateProcessingProgress(_ progress: Double) {
        DispatchQueue.main.async {
            self.processingProgress = progress
        }
    }

    func updateIndexingProgress(_ progress: Double) {
        DispatchQueue.main.async {
            self.indexingProgress = progress
        }
    }

    func incrementWaitingFiles() {
        DispatchQueue.main.async {
            self.waitingFilesCount += 1
        }
    }

    func incrementFinishedFiles() {
        DispatchQueue.main.async {
            self.finishedFilesCount += 1
            self.waitingFilesCount = max(0, self.waitingFilesCount - 1)
        }
    }

    func reset() {
        DispatchQueue.main.async {
            self.processingProgress = 0.0
            self.indexingProgress = 0.0
            self.waitingFilesCount = 0
            self.finishedFilesCount = 0
        }
    }
}
