#!/usr/bin/env python3

import aws_cdk as cdk

from logs_memory_leak.logs_memory_leak_stack import LogsMemoryLeakStack


app = cdk.App()
LogsMemoryLeakStack(app, "LogsMemoryLeakStack")

app.synth()
