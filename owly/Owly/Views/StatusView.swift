import SwiftUI

struct StatusView: View {
    @ObservedObject var directoriesViewModel: DirectoriesViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Processing Progress")
            ProgressView(value: directoriesViewModel.processingProgress)
                .progressViewStyle(LinearProgressViewStyle())
            
            Text("Indexing Progress")
            ProgressView(value: directoriesViewModel.indexingProgress)
                .progressViewStyle(LinearProgressViewStyle())
            
            HStack {
                Text("Unprocessed Images")
                Spacer()
                Text("\(directoriesViewModel.unprocessedImageCount)")
                    .padding(8)
                    .background(Color.red)
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
        StatusView(directoriesViewModel: DirectoriesViewModel())
    }
}
