workspace "orders-api" "Order handling for the shop backend." {

    !identifiers hierarchical

    model {
        customer = person "Customer" "Views their orders and applies discounts."
        operator = person "Operator" "Runs maintenance scripts from the repository root."

        gateway = softwareSystem "Shop gateway" "Hosts the shop's HTTP endpoints and resolves session cookies to user IDs. Separate repository." "External"

        orders = softwareSystem "Orders service" "Order handling for the shop backend." {
            api = container "Orders API" "Order request handlers, loaded and called by the shop gateway. Trusts request.userId, which the gateway sets from the session." "TypeScript, Node.js" {
                routes = component "Routes" "src/routes.ts: maps GET /orders/:id and POST /orders/:id/discount to handlers." "TypeScript"
                orderHandlers = component "Order handlers" "src/handlers/orders.ts: call the order service, format totals and map errors." "TypeScript"
                errorMapping = component "Error mapping" "src/handlers/errors.ts: maps domain errors to 404 and 400, rethrows the rest." "TypeScript"
                orderService = component "Order service" "src/services/orders.ts: business rules for orders, including the ownership check." "TypeScript"
                money = component "Money" "src/money.ts: parses decimal strings to whole cents with integer arithmetic, and formats cents." "TypeScript"
                storage = component "Storage" "src/db.ts: reads and writes the orders file. Only services may use it." "TypeScript"
            }

            data = container "Orders file" "data/orders.json (or $ORDERS_DB): orders and refunds." "JSON file" "FileStore"
            backup = container "Backup script" "scripts/backup-db.sh: copies the data directory to a timestamped snapshot." "Bash"
            backups = container "Backup snapshots" "backups/<UTC timestamp>/" "File system" "FileStore"
        }

        customer -> gateway "Uses the shop through" "HTTPS"
        gateway -> orders.api.routes "Calls order handlers with the user ID" "Function call"
        orders.api.routes -> orders.api.orderHandlers "Dispatches GET /orders/:id and POST /orders/:id/discount to" "In-process call"
        orders.api.orderHandlers -> orders.api.orderService "Reads and updates the user's orders through" "In-process call"
        orders.api.orderHandlers -> orders.api.money "Formats totals with" "In-process call"
        orders.api.orderHandlers -> orders.api.errorMapping "Maps domain errors with" "In-process call"
        orders.api.orderService -> orders.api.storage "Reads and writes orders through" "In-process call"
        orders.api.orderService -> orders.api.money "Parses discount amounts with" "In-process call"
        orders.api.storage -> orders.data "Reads and writes" "File system"

        operator -> orders.backup "Runs" "Shell"
        orders.backup -> orders.data "Reads" "cp -R"
        orders.backup -> orders.backups "Writes timestamped snapshots to" "cp -R"
    }

    views {
        systemContext orders "SystemContext" {
            include * customer
            autolayout lr
        }

        container orders "Containers" {
            include *
            autolayout lr
        }

        component orders.api "OrdersApiComponents" {
            include * customer
            autolayout lr
        }

        styles {
            element "Person" {
                shape person
            }
            element "FileStore" {
                shape folder
            }
            element "External" {
                background #999999
                color #ffffff
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
