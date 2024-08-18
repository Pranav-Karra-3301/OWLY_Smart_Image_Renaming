import SwiftUI

struct ContentView: View {
    @State private var selectedSection: String? = "Search"

    var body: some View {
        NavigationView {
            List {
                NavigationLink(destination: SearchView(), tag: "Search", selection: $selectedSection) {
                    Label("Search", systemImage: "magnifyingglass")
                }
                NavigationLink(destination: StatisticsView(), tag: "Statistics", selection: $selectedSection) {
                    Label("Statistics", systemImage: "chart.bar")
                }
                NavigationLink(destination: PreferencesView(), tag: "Preferences", selection: $selectedSection) {
                    Label("Preferences", systemImage: "gear")
                }
                NavigationLink(destination: APIKeyView(), tag: "APIKey", selection: $selectedSection) {
                    Label("API Key", systemImage: "key")
                }
                NavigationLink(destination: DirectoriesView(), tag: "Directories", selection: $selectedSection) {
                    Label("Directories", systemImage: "folder")
                }
                NavigationLink(destination: StatusView(), tag: "Status", selection: $selectedSection) {
                    Label("Status", systemImage: "clock")
                }
                NavigationLink(destination: AboutView(), tag: "About", selection: $selectedSection) {
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
