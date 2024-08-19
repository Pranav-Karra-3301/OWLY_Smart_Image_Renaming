import SwiftUI

class StatusViewModel: ObservableObject {
    @Published var processingProgress: Double = 0.0
    @Published var indexingProgress: Double = 0.0
    @Published var waitingFilesCount: Int = 0
    @Published var finishedFilesCount: Int = 0
}

struct StatusView: View {
    @ObservedObject var viewModel: StatusViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Processing Progress")
            ProgressView(value: viewModel.processingProgress)
                .progressViewStyle(LinearProgressViewStyle())
            
            Text("Indexing Progress")
            ProgressView(value: viewModel.indexingProgress)
                .progressViewStyle(LinearProgressViewStyle())
            
            HStack {
                Text("Waiting Files")
                Spacer()
                Text("\(viewModel.waitingFilesCount)")
                    .padding(8)
                    .background(Color.orange)
                    .foregroundColor(.white)
                    .clipShape(Circle())
            }
            
            HStack {
                Text("Finished Files")
                Spacer()
                Text("\(viewModel.finishedFilesCount)")
                    .padding(8)
                    .background(Color.green)
                    .foregroundColor(.white)
                    .clipShape(Circle())
            }
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
    }
}

struct StatusView_Previews: PreviewProvider {
    static var previews: some View {
        StatusView(viewModel: StatusViewModel())
    }
}
