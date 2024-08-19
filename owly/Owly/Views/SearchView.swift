import SwiftUI
import CoreData

struct SearchView: View {
    @ObservedObject var directoriesViewModel: DirectoriesViewModel
    @State private var searchQuery = ""
    @State private var searchResults: [FileIndex] = []
    @Environment(\.managedObjectContext) private var viewContext

    var body: some View {
        VStack {
            TextField("Search files...", text: $searchQuery, onCommit: {
                searchFiles(query: searchQuery)
            })
            .textFieldStyle(RoundedBorderTextFieldStyle())
            .padding()

            List(searchResults, id: \.self) { result in
                VStack(alignment: .leading) {
                    Text("Current file name: \(result.name ?? "N/A")")
                    Text("Old file name: \(result.path ?? "N/A")")
                    Text("Image description: \(result.describe ?? "N/A")")
                    Text("OCR: \(result.ocr ?? "N/A")")
                    Text("Keywords: \(result.tags ?? "N/A")")
                    Text("Timestamp: \(result.timestamp?.description ?? "N/A")")
                }
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .onAppear(perform: loadRecentFiles)
        .onReceive(NotificationCenter.default.publisher(for: .newFilesProcessed)) { _ in
            loadRecentFiles()
        }
    }

    private func loadRecentFiles() {
        let fetchRequest: NSFetchRequest<FileIndex> = FileIndex.fetchRequest()
        fetchRequest.sortDescriptors = [NSSortDescriptor(keyPath: \FileIndex.timestamp, ascending: false)]
        fetchRequest.fetchLimit = 20  // Adjust this number as needed

        do {
            searchResults = try viewContext.fetch(fetchRequest)
        } catch {
            print("Error fetching recent files: \(error)")
        }
    }

    private func searchFiles(query: String) {
        let fetchRequest: NSFetchRequest<FileIndex> = FileIndex.fetchRequest()
        fetchRequest.predicate = NSPredicate(format: "name CONTAINS[cd] %@ OR describe CONTAINS[cd] %@ OR tags CONTAINS[cd] %@ OR ocr CONTAINS[cd] %@", query, query, query, query)

        do {
            searchResults = try viewContext.fetch(fetchRequest)
        } catch {
            print("Error fetching search results: \(error)")
        }
    }
}

struct SearchView_Previews: PreviewProvider {
    static var previews: some View {
        SearchView(directoriesViewModel: DirectoriesViewModel())
            .environment(\.managedObjectContext, PersistenceController.preview.container.viewContext)
    }
}
