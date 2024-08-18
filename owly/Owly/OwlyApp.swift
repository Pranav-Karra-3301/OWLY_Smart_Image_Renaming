//
//  OwlyApp.swift
//  Owly
//
//  Created by Pranav Karra on 8/18/24.
//

import SwiftUI

@main
struct OwlyApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
