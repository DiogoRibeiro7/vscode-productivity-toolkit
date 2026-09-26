declare module 'fs-extra';

declare module 'mocha' {
    interface MochaOptions {
        ui?: string;
        color?: boolean;
        timeout?: number;
        reporter?: string;
    }

    class Mocha {
        constructor(options?: MochaOptions);
        addFile(file: string): this;
        run(callback?: (failures: number) => void): unknown;
    }

    export = Mocha;
}

declare function suite(name: string, callback: () => void): void;
declare function setup(callback: () => void | Promise<void>): void;
declare function teardown(callback: () => void | Promise<void>): void;
declare function test(name: string, callback: () => void | Promise<void>): void;
