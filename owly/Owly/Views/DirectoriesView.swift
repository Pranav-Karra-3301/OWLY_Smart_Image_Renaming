import SwiftUI
import Combine

struct DirectoriesView: View {
    @ObservedObject var viewModel: DirectoriesViewModel
    @ObservedObject var statusViewModel: StatusViewModel
    
    var body: some View {
        VStack {
            List {
                ForEach($viewModel.directories) { $directory in
                    HStack {
                        Text(directory.path)
                        Spacer()
                        Toggle("", isOn: $directory.isWatched)
                            .labelsHidden()
                            .onChange(of: directory.isWatched) { newValue in
                                if newValue {
                                    viewModel.startWatching(directory: directory)
                                }
                                viewModel.saveDirectories()
                            }
                    }
                    .modifier(TransparentListStyle())
                }
                .onDelete(perform: viewModel.removeDirectories)
            }
            .listStyle(SidebarListStyle())
            .background(Color.clear)
            
            HStack {
                Button("Add Directory") {
                    viewModel.addDirectory()
                }
                
                Button("Process Files") {
                    viewModel.processFiles(statusViewModel: statusViewModel)
                }
                .disabled(viewModel.isProcessing)
            }
            .padding()
        }
        .frame(minWidth: 250, idealWidth: 300, maxWidth: .infinity, minHeight: 300, idealHeight: 400, maxHeight: .infinity)
        .background(VisualEffectView(material: .hudWindow, blendingMode: .behindWindow))
        .onAppear {
            viewModel.loadDirectories()
        }
    }
}

struct DirectoriesView_Previews: PreviewProvider {
    static var previews: some View {
        DirectoriesView(viewModel: DirectoriesViewModel(), statusViewModel: StatusViewModel())
    }
}
