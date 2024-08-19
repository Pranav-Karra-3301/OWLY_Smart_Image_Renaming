import SwiftUI

struct ContentView: View {
    @StateObject private var directoriesViewModel = DirectoriesViewModel()
    @StateObject private var statusViewModel = StatusViewModel()

    var body: some View {
        NavigationView {
            List {
                NavigationLink(destination: SearchView(directoriesViewModel: directoriesViewModel)) {
                    Label("Search", systemImage: "magnifyingglass")
                }
                NavigationLink(destination: StatisticsView()) {
                    Label("Statistics", systemImage: "chart.bar")
                }
                NavigationLink(destination: PreferencesView()) {
                    Label("Preferences", systemImage: "gear")
                }
                NavigationLink(destination: APIKeyView()) {
                    Label("API Key", systemImage: "key")
                }
                NavigationLink(destination: DirectoriesView(viewModel: directoriesViewModel, statusViewModel: statusViewModel)) {
                    Label("Directories", systemImage: "folder")
                }
                NavigationLink(destination: StatusView(viewModel: statusViewModel)) {
                    Label("Status", systemImage: "clock")
                }
                NavigationLink(destination: AboutView()) {
                    Label("About", systemImage: "info.circle")
                }
            }
            .listStyle(SidebarListStyle())

            Text("Select a section")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .frame(minWidth: 800, minHeight: 600)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
